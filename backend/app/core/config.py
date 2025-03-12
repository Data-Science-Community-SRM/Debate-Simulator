from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Debate Simulator"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    OPENAI_API_KEY: str = ""
    LOCAL_MODEL_PATH: str = "models/"

    class Config:
        env_file = ".env"

settings = Settings()