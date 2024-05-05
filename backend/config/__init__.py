from pydantic_settings import BaseSettings 


class CommonSettings(BaseSettings):
    APP_NAME: str = "FARM Board"
    DEBUG_MODE: bool = False
    APP_MODE: str = "poster"


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_KEYS: str
    FRONTEND_BUILD_PATH: str = "../frontend/build"
    FRONTEND_TITLE: str = "FARM Board"
    FRONTEND_SHORTNAME: str = "farm-board"
    FRONTEND_DESCRIPTION: str = "Status board built with Fast API React Mongodb"
    FRONTEND_POSTS_NAME: str = "FARM Board Posts"

class DatabaseSettings(BaseSettings):
    DB_URL: str
    DB_NAME: str


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
