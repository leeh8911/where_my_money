from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    timezone: str = "Asia/Seoul"
    log_format: str = "text"



def get_settings() -> Settings:
    return Settings(
        timezone=os.getenv("APP_TIMEZONE", "Asia/Seoul"),
        log_format=os.getenv("LOG_FORMAT", "text"),
    )
