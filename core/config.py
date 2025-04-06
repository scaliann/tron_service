from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import BaseModel
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR

class DbSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    echo: bool = True


class Settings(BaseSettings):
    db: DbSettings = DbSettings()

settings = Settings()
