from linebot.v3.messaging import MessagingApi, ApiClient, ReplyMessageRequest, TextMessage
from docs import append_rating_record
from datetime import datetime
class PostbackHandler:
    def __init__(self, db,configuration):
        self.db = db
        self.configuration = configuration

    async def handle(self, event):
        user_id = event.source.user_id

        if user_id in self.db.userNeedRatings:
            await self.handle_rating(event)

    async def handle_rating(self, event):
        self.db.userNeedRatings.remove(event.source.user_id)
        score = event.postback.data
        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f"感謝您的評分：{score}")]
                )
            )
        user_info = await self.db.add_rating_record(event.source.user_id, score)
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        append_rating_record(user_info['name'], score, current_time)

        
        # record = await self.db.increment_column("rating_record", "line_id", event.source.user_id, f"score{score}")
        # record_rating(record["name"], int(score), record[f"score{score}"])