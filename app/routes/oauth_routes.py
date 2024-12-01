from fastapi import APIRouter, Request, HTTPException, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from requests_oauthlib import OAuth2Session
import requests
from config import settings
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import clear_token, decode_token, normalize_name, send_async_request

router = APIRouter()

# OAuth 配置
CLIENT_ID = settings.OAUTH2_CLIENT_ID
CLIENT_SECRET = settings.OAUTH2_CLIENT_SECRET
AUTHORIZATION_BASE_URL = settings.OAUTH2_AUTHORIZATION_URL
TOKEN_URL = settings.OAUTH2_TOKEN_URL
REDIRECT_URI = settings.OAUTH2_REDIRECT_URI
RESOURCE = settings.OAUTH2_RESOURCE
USER_INFO_URL = settings.OAUTH2_USER_INFO_URL
LOGOUT_URL = settings.OAUTH2_LOGOUT_URL

async def get_templates(request: Request):
    return request.app.state.templates

@router.get("/register", response_class=RedirectResponse)
def index(request: Request):
    session = request.session
    session.clear()
    clear_token(session)
    chat_id = request.query_params.get("chat_id")
    if chat_id:
        session["chat_id"] = chat_id
    logout_redirect = f"https://fs.ncku.edu.tw/adfs/ls/?wa=wsignout1.0&wreply=https://chatbot.oia.ncku.edu.tw/register/start-auth"
    return RedirectResponse(url=logout_redirect)


@router.get("/register/start-auth", response_class=RedirectResponse)
def start_auth(request: Request):
    session = request.session
    chat_id = session.get("chat_id")
    if not chat_id:
        raise HTTPException(status_code=400, detail="No chat_id found in session")

    ncku = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    authorization_url, state = ncku.authorization_url(
        AUTHORIZATION_BASE_URL, resource=RESOURCE
    )
    print(authorization_url)
    session["oauth_state"] = state
    session["chat_id"] = chat_id
    return RedirectResponse(url=authorization_url)


@router.get("/register/callback", response_class=RedirectResponse)
def register_callback(request: Request):
    authorization_code = request.query_params.get("code")
    try:
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
        response = requests.post(TOKEN_URL, data=data)
        if response.status_code == 200:
            token = response.json()
            request.session["access_token"] = token
            return RedirectResponse(url="/register/fill-form")
        else:
            raise HTTPException(
                status_code=400, detail=f"Failed to fetch token: {response.json()}"
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch token: {str(e)}")


@router.get("/register/fill-form", response_class=HTMLResponse)
def fill_form(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    if "access_token" not in request.session:
        raise HTTPException(
            status_code=400, detail="User info not found in the session"
        )

    token = request.session.get("access_token")
    user_info = decode_token(token["access_token"])
    user_info["normalized_name"] = normalize_name(
        user_info["DisplayName"], user_info["studentStuEnName"]
    )
    return templates.TemplateResponse(
        "fill_form.html", {"request": request, "user_info": user_info}
    )

@router.post("/register/submit-info", response_class=HTMLResponse)
async def submit_info(
    request: Request,
    name: str = Form(...),
    department: str = Form(...),
    student_id: str = Form(...),
    line_name: str = Form(...),
    nationality: str = Form(...),
    Language: str = Form(...),
    Status: str = Form(...),
    templates: Jinja2Templates = Depends(get_templates)
):
    session = request.session
    chat_id = session.get("chat_id")

    if not all(
        [
            name,
            department,
            student_id,
            line_name,
            nationality,
            Language,
            Status,
            chat_id,
        ]
    ):
        return templates.TemplateResponse("submission_error.html", {"request": request})

    redirect_url = f"https://chatbot.oia.ncku.edu.tw/sign_up/student/{nationality}&{student_id}&{name}&{department}&{line_name}&{Language}&{Status}&{chat_id}"

    try:
        response_text = await send_async_request(redirect_url)
        if response_text:
            return templates.TemplateResponse(
                "submission_success.html", {"request": request}
            )
        else:
            return templates.TemplateResponse(
                "submission_error.html", {"request": request}
            )
    except Exception as e:
        return templates.TemplateResponse("submission_error.html", {"request": request})
