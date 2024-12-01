import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
load_dotenv()

class Settings(BaseSettings):
    # 應用程序設置
    APP_NAME: str = "OIA Chatbot"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    # OAuth 設置
    OAUTH2_CLIENT_ID: str = os.getenv("OAUTH2_CLIENT_ID")
    OAUTH2_CLIENT_SECRET: str = os.getenv("OAUTH2_CLIENT_SECRET")
    OAUTH2_AUTHORIZATION_URL: str = os.getenv("OAUTH2_AUTHORIZATION_URL")
    OAUTH2_TOKEN_URL: str = os.getenv("OAUTH2_TOKEN_URL")
    OAUTH2_REDIRECT_URI: str = os.getenv("OAUTH2_REDIRECT_URI")
    OAUTH2_RESOURCE: str = os.getenv("OAUTH2_RESOURCE")
    OAUTH2_USER_INFO_URL: str = os.getenv("OAUTH2_USER_INFO_URL")
    OAUTH2_LOGOUT_URL: str = os.getenv("OAUTH2_LOGOUT_URL")

    # LINE Bot 設置
    LINE_CHANNEL_SECRET: str = os.getenv("LINE_CHANNEL_SECRET")
    LINE_CHANNEL_ACCESS_TOKEN: str = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    # LIFF 設置
    LIFF_SIGN_UP: str = os.getenv("LIFF_SIGN_UP")
    LIFF_NON_STUDENT_SIGN_UP: str = os.getenv("LIFF_NON_STUDENT_SIGN_UP")
    LIFF_ESACALATION: str = os.getenv("LIFF_ESACALATION")

    #openai
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_API_TYPE: str=os.getenv("OPENAI_API_TYPE")
    AZURE_ENDPOINT_EMBEDDINGS: str=os.getenv("AZURE_ENDPOINT_EMBEDDINGS")
    AZURE_ENDPOINT_LLM: str=os.getenv("AZURE_ENDPOINT_LLM")

    # 其他設置
    TEMPLATE_DIR: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    STATIC_DIR: str = "static"

    class Config:
        env_file = ".env"

settings = Settings()
