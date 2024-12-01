import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from asyncdatabase import Database
from app.services.line_bot_service.richmenu import set_rich_menu
from config import settings
from datetime import datetime
from fastapi.responses import FileResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

async def get_db(request: Request):
    return request.app.state.db

async def get_templates(request: Request):
    return request.app.state.templates

class StatusChange(BaseModel):
    user_id: str
    change_type: str


@router.get("/error", response_class=HTMLResponse)
async def error(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    return templates.TemplateResponse(
        "error.html", {"request": request, "liff_id": settings.LIFF_ESACALATION}
    )

@router.get("/error/{user_id}")
async def error_response(user_id: str, db: Database = Depends(get_db)):
    user_info=await db.get_user_info(user_id)
    if 'todo:1'not in user_info['mode']:
        try:
            user_info = await db.update_data_and_get_info(
                "info", "line_id", user_id, {"mode": "todo:1,disabled:0"}
            )
            print(user_info["last_message"])
            set_rich_menu(user_info["language"] + "-escalation", user_id)
        except Exception as e:
            print(e)
        return {"response": "ok"}
    else:
        return {"command": "cancel"}

@router.get("/error/cancel/{user_id}")
async def remove_todo_by_user(user_id: str, db: Database = Depends(get_db)):
    user_info = await db.update_data_and_get_info(
        "info", "line_id", user_id, {"mode": "todo:0,disabled:0"}
    )
    set_rich_menu(user_info["language"], user_id)
    return "ok"

@router.post("/error/complete")
async def complete_todo(statuschange: StatusChange, db: Database = Depends(get_db)):
    try:
        user_id = statuschange.user_id
        type_ = statuschange.change_type
        if type_ == "0":
            await db.update_data(
                "info", "line_id", user_id, {"mode": "todo:0,disabled:0"}
            )
            print(user_id + "complete")
    except Exception as E:
        pass
    return "ok"
