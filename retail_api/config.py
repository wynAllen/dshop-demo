from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "retail-api"
    debug: bool = False

    model_config = {"env_prefix": "RETAIL_"}


settings = Settings()
