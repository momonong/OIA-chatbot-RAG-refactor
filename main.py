import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from config import settings
from asyncdatabase import Database
from contextlib import asynccontextmanager
from app.routes import oauth_routes, line_bot_routes, signup_routes, error_routes,admin_routes
from linebot.v3.messaging import Configuration
from app.services.line_bot_service.handlers import EventHandler
from app.services.line_bot_service.richmenu import initialize_rich_menu
from fastapi.middleware.cors import CORSMiddleware
import logging


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
database = Database()
# Setup logging
logging.basicConfig(level=logging.DEBUG)
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    app.state.db = database
    await initialize_rich_menu(database)
    configuration = Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)
    app.state.event_handler = EventHandler(database,configuration)
    app.state.templates = templates
    yield
    await database.close()

# 創建 FastAPI 應用實例
app = FastAPI(lifespan=lifespan)

# 設置會話中間件
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://140.116.249.221:5173","https://localhost:5173"],  # 允許的源
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有方法
    allow_headers=["*"],  # 允許所有頭
)

app.mount("/assets", StaticFiles(directory=os.path.join(BASE_DIR, "dist","assets")), name="assets")





# 註冊路由
app.include_router(oauth_routes.router)
app.include_router(line_bot_routes.router)
app.include_router(signup_routes.router)
app.include_router(error_routes.router)
app.include_router(admin_routes.router)


@app.get("/oia-form")
async def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "dist","index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
