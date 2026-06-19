from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    encryption_key: str
    environment: str = "dev"
    jwt_algorithm: str = "HS256"
    jwt_expire_days: int = 30

    model_config = {"env_file": ".env"}


settings = Settings()
