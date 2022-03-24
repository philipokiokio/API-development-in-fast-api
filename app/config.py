from pydantic import BaseSettings

class Settings(BaseSettings):
    
    database_username: str
    database_password: str
    database_hostname: str
    database_name: str
    database_port: str
    secret_key: str
    algorithm: str
    access_token_minutes: str

    class Config:
        env_file = ".env"




settings = Settings()