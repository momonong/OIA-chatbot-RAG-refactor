import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import logging
from fastapi import APIRouter, Request, Depends, HTTPException
from config import settings
from asyncdatabase import Database
from linebot.v3.webhook import WebhookParser
from linebot.v3.exceptions import InvalidSignatureError
from app.services.line_bot_service.handlers import EventHandler


router = APIRouter()

parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


async def get_db(request: Request):
    return request.app.state.db

async def get_event_handler(request: Request):
    return request.app.state.event_handler

@router.post("/message-callback")
async def callback(request: Request, db: Database = Depends(get_db), event_handler: EventHandler = Depends(get_event_handler)):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    body = body.decode("utf-8")
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        start = time.time()
        await event_handler.handle_event(event)
        end = time.time()
        logging.info(f"處理事件耗時：{end - start}")
    return "OK"







