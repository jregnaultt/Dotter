import os
from pydantic import BaseModel

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class Settings(BaseModel):
    PROJECT_NAME: str = "Fighting Game Sprite Generator API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    POLLINATIONS_API_KEY: str = os.getenv("POLLINATIONS_API_KEY", "")
    POLLINATIONS_MODEL: str = os.getenv("POLLINATIONS_MODEL", "kontext")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "output_sprites")
    
settings = Settings()
