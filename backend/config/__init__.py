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

class DatabaseSettings(BaseSettings):
    DB_URL: str
    DB_NAME: str


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
