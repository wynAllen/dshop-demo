from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "retail-api"
    debug: bool = False
    database_url: str = "sqlite:///./retail.db"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7

    model_config = {"env_prefix": "RETAIL_"}


settings = Settings()
