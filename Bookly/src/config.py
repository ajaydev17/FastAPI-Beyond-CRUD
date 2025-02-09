from pydantic_settings import BaseSettings, SettingsConfigDict


# define a settings class
class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )


# create an instance of configuration
Config = Settings()
