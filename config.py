from pydantic import BaseSettings

class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    MONGO_URL: str = ""  # optional for now

    class Config:
        env_file = ".env"

settings = Settings()
