from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    exchanges: list[str] = ["bybit", "okx"]
    base_asset: str = "USDT"
    min_net_profit: float = 0.3

    model_config = SettingsConfigDict(env_prefix="", env_file=".env")


settings = Settings()
