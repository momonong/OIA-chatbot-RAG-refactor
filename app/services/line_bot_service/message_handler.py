import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import random
from datetime import datetime
from linebot.v3.messaging import MessagingApi, ApiClient, ReplyMessageRequest
from linebot import LineBotApi
from app.services.line_bot_service.messages import NotifyRegisterMessage, EscalationMessage, RatingMessage, NormalMessage
from app.services.line_bot_service.richmenu import set_rich_menu
from app.services.line_bot_service.NormalQA.retriver import Retriever
from config import settings
from docs import log
import logging


class MessageHandler:
    def __init__(self, db,configuration):
        self.db = db
        self.configuration = configuration
        self.retriever = Retriever()

    async def handle(self, event):
        if event.message.type == 'text':
            await self.handle_text_message(event)

    async def handle_text_message(self, event):
        start = time.time()
        user_id = event.source.user_id
        question = event.message.text
        user_info = await self.db.get_user_info(user_id)

        if not user_info:
            await self.send_register_notification(event)
            return

        if user_info["mode"].split(",")[1] == "disabled:1":
            logging.info(f"{user_id} is disabled")
            return

        if user_info["mode"].split(",")[0] == "todo:1":
            await self.send_escalation_status(event, user_info["language"])
            return

        if question == "switch language":
            await self.switch_language(user_id, user_info["language"])
        else:
            await self.process_message(event, user_info, question, start)

    async def send_register_notification(self, event):
        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[NotifyRegisterMessage().create_message()]
                )
            )

    async def send_escalation_status(self, event, language):
        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[EscalationMessage(language).create_escalation_status_message()]
                )
            )

    async def switch_language(self, user_id, current_language):
        new_language = "en" if current_language == "zh" else "zh"
        await self.db.update_data("info", "line_id", user_id, {"language": new_language})
        set_rich_menu(new_language,user_id)

    async def process_message(self, event, user_info, question, start):
        identity = user_info["identity"]
        frequency = user_info["frequency"]
        language = user_info["language"]
        
        response = self.retriever.get_reply(f"{identity.split(',')[0]}_{language}", question)
        
        if frequency >= random.randint(1, 10):
            await self.send_rating_message(event, user_info, response, question)
        else:
            await self.send_normal_message(event, user_info, response, question)
        
        end = time.time()
        log(question, response, end - start, user_info["name"], user_info["mode"])

    async def send_rating_message(self, event, user_info, response, question):
        rating_message = RatingMessage.create_rating_message(response, user_info["language"])
        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        line_bot_api.reply_message(event.reply_token, rating_message)
        self.db.userNeedRatings.append(user_info["line_id"])
        await self.db.update_data(
            "info",
            "line_id",
            user_info["line_id"],
            {
                "frequency": 0,
                "last_message": question,
                "last_used": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
        )

    async def send_normal_message(self, event, user_info, response, question):
        normal_message = NormalMessage.create_normal_message(response, user_info["language"])
        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[normal_message]
                )
            )
        
        await self.db.update_data(
            "info",
            "line_id",
            user_info["line_id"],
            {
                "frequency": user_info["frequency"] + 1,
                "last_message": question,
                "last_used": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
        )
