from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    TEST_MOTION: str = "Artificial Intelligence will benefit humanity more than harm it"
    TEST_MAX_ROUNDS: int = 3
    
    class Config:
        env_file = ".env.test"

test_settings = TestSettings()