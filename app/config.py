from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_password: str
    database_name: str
    database_username: str
    database_port: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

settings = Settings()