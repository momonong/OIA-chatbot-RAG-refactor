import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import urllib.parse
from datetime import datetime
from fastapi import Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.line_bot_service.richmenu import set_rich_menu
from config import settings
from fastapi import APIRouter
from asyncdatabase import Database

router = APIRouter()

async def get_db(request: Request):
    return request.app.state.db


async def get_templates(request: Request):
    return request.app.state.templates


@router.get("/sign_up/student", response_class=HTMLResponse)
async def student_sign_up(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    print("in sign_up [python output]")
    return templates.TemplateResponse(
        "start.html", {"request": request, "liff_id": settings.LIFF_SIGN_UP}
    )


@router.get("/sign_up/student/{info}")
async def register_in_system(info: str, db: Database = Depends(get_db)):
    print(info)
    info = urllib.parse.unquote(info)
    nationality, student_id, name, department, line_name, language, status, user_id = (
        info.split("&")
    )
    status = {
        "1": "oversea_chinese_students",
        "2": "international_students",
        "3": "chinese_students",
    }[status]
    data_to_insert = {
        "department": department,
        "student_id": student_id,
        "identity": status,
        "last_used": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "line_id": user_id,
        "mode": "todo:0,disabled:0",
        "nationality": nationality,
        "frequency": 0,
        "last_message": "",
        "language": language,
        "line_name": line_name,
        "is_student": 1,
    }
    await db.insert_data("info", data_to_insert)
    set_rich_menu(language, user_id)
    return {"response": "ok"}


@router.get("/sign_up/non_student", response_class=HTMLResponse)
async def non_student_sign_up(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    print("non_studentt in sign_up ")
    return templates.TemplateResponse(
        "fill_form_non_student.html",
        {"request": request, "liff_id": settings.LIFF_NON_STUDENT_SIGN_UP},
    )


@router.post("/sign_up/non_student/fill_form", response_class=HTMLResponse)
async def submit_info(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
    name: str = Form(...),
    line_name: str = Form(...),
    language: str = Form(...),
    identity: str = Form(...),
    user_id: str = Form(...),
    status: str = Form(...),
    db: Database = Depends(get_db),
):
    if not all([name, line_name, language, user_id, identity, status]):
        print("\n\nMissing form data or chat_id.\n\n")
        return templates.TemplateResponse("submission_error.html", {"request": request})
    print(
        f"Name: {name}, Line Name: {line_name}, Language: {language}, Identity: {identity}, User ID: {user_id}"
    )
    status = {
        "1": "oversea_chinese_students",
        "2": "international_students",
        "3": "chinese_students",
    }[status]
    try:
        data_to_insert = {
            "department": "",
            "student_id": "",
            "identity": status + "," + identity,
            "last_used": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "line_id": user_id,
            "mode": "todo:0,disabled:0",
            "nationality": "",
            "frequency": 0,
            "last_message": "",
            "language": language,
            "line_name": line_name,
            "is_student": 0,
        }
        await db.insert_data("info", data_to_insert)
        set_rich_menu(language, user_id)
        return templates.TemplateResponse(
            "submission_success.html", {"request": request}
        )
    except Exception as e:
        print(f"\n\nError during register: {str(e)}\n\n")
        return templates.TemplateResponse("submission_error.html", {"request": request})









