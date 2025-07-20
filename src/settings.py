from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    GLANCES_URL: str

    class Config:
        env_file = '.env'


settings = Settings()

if __name__ == '__main__':
    print(settings.model_dump_json(indent=2))
    print('Settings loaded successfully.')
