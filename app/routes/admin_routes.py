import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from asyncdatabase import Database
from app.services.line_bot_service.richmenu import set_rich_menu
from config import settings
from datetime import datetime
from fastapi.responses import FileResponse



router = APIRouter()
async def get_db(request: Request):
    return request.app.state.db


async def get_templates(request: Request):
    return request.app.state.templates

@router.get("/get_all_users", response_class=JSONResponse)
async def get_users_info(request: Request, db: Database = Depends(get_db)):
    users = await db.get_all_users_info('info')
    for user in users:
        user['line_bot_mode'] =  'disabled:0' in user['mode']
        user['need_assistance'] = 'todo:1' in user['mode']
        user['student_id'] = 'non_student' if user['student_id'] is None else user['student_id']
        user['identity'] = {'oversea_chinese_students':'僑生',
        'chinese_students':'陸生',
        'international_students':'國際生',
        'oversea_chinese_students,unenrolled Freshmen':'未註冊新生(僑生)',
        'oversea_chinese_students,other':'其他(僑生)',
        'oversea_chinese_students,parent':'家長(僑生)',
        'chinese_students,unenrolled Freshmen':'未註冊新生(陸生)',
        'chinese_students,other':'其他(陸生)',
        'chinese_students,parent':'家長(陸生)',
        'international_students,unenrolled Freshmen':'未註冊新生(國際生)',
        'international_students,other':'其他(國際生)',
        'international_students,parent':'家長(國際生)'
        }[user['identity']]

    json_data = {
        "data": [
            {
                "student_id": user['student_id'],
                "name": user['name'],
                "last_message": user['last_message'],
                "line_bot_mode": user['line_bot_mode'],
                "need_assistance": user['need_assistance'],
                "line_name": user['line_name'],
                "identity": user['identity'],
                "last_used": user['last_used'].strftime("%Y-%m-%d %H:%M:%S") if user['last_used'] else "",
                "line_id": user['line_id']
            } for user in users
        ]
    }
    return JSONResponse(content=json_data)



class StatusUpdate(BaseModel):
    user_id: str
    status_type: str
    status: bool


@router.post("/update-status")
async def update_status(request:Request,status_update:StatusUpdate,db: Database = Depends(get_db)):
    user_id = status_update.user_id
    status_type = status_update.status_type
    status = status_update.status
    if(status_type == "Chatbot_status"):
        print(status_type)
        print(status)
        if status:
            await db.update_data("info", "line_id", user_id, {"mode": "todo:1,disabled:1"})
        else:
            await db.update_data("info", "line_id", user_id, {"mode": "todo:1,disabled:0"})
        return "ok"
    elif(status_type == "Human_service"):
        print(status_type)
        print(status)
        if status:
            await db.update_data("info", "line_id", user_id, {"mode": "todo:0,disabled:0"})
        return "ok"
    else:
        raise HTTPException(status_code=400, detail="無效的狀態類型")
