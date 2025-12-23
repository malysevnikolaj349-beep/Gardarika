from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_token: str = ""
    admin_ids: str = ""
    admin_webapp_token: str = "change-me"
    webapp_host: str = "0.0.0.0"
    webapp_port: int = 8080
    database_path: str = "gardarika.db"
    base_url: str = "http://localhost:8080"

    @property
    def admin_id_list(self) -> list[int]:
        if not self.admin_ids:
            return []
        return [int(part.strip()) for part in self.admin_ids.split(",") if part.strip()]


settings = Settings()
