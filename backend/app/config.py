from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    MISTRAL_API_KEY: str

    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str

    BASE_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()