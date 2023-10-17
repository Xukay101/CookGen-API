from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "CookGen-API"

    # Getting .env variables
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

    BASE_URL: str

    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASS: str

    JWT_SECRET_KEY: str # openssl rand -hex 32
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRE_MINUTES: int = 30

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASS: str

settings = Settings()
