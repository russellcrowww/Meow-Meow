import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Общие настройки
    app_name: str = "Mica"
    debug: bool = True 
    
    # БД - убрали aiosqlite, чтобы не конфликтовать с синхронным create_engine
    database_url: str = "sqlite:///./Mica_sys.db"
    
    # Безопасность
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    
    # Пути
    static_dir: str = "static"
    images_dir: str = "static/images"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Создаем экземпляр настроек
settings = Settings()

# Автоматическое создание папок, чтобы сервер не падал при старте
os.makedirs(settings.images_dir, exist_ok=True)