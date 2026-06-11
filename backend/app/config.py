from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://forex:forex_pass@localhost:5432/forex"
    exchange_api_url: str = "https://open.er-api.com/v6/latest/USD"
    default_api_key: str = "demo-key"

    class Config:
        env_file = ".env"


settings = Settings()
