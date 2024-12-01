import logging
from linebot.v3.webhooks import MessageEvent, PostbackEvent
from app.services.line_bot_service.message_handler import MessageHandler
from app.services.line_bot_service.postback_handler import PostbackHandler

class EventHandler:
    def __init__(self, db,configuration):
        self.db = db
        self.configuration = configuration
        self.message_handler = MessageHandler(db,configuration)
        self.postback_handler = PostbackHandler(db,configuration)
        

    async def handle_event(self, event):
        if isinstance(event, MessageEvent):
            await self.message_handler.handle(event)
        elif isinstance(event, PostbackEvent):
            await self.postback_handler.handle(event)
        else:
            logging.warning(f"未處理的事件類型：{type(event)}")