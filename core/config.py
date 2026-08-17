from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Configuración global del sistema MORA.
    Lee automáticamente las variables de entorno o un archivo .env local.
    """
    PROJECT_NAME: str = "MORA API"
    VERSION: str = "0.2.0"
    REDIS_BROKER_URL: str = "redis://localhost:6379/0"
    REDIS_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Configuración para leer archivos .env automáticamente
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Instancia global de configuración reutilizable en todo el proyecto
settings = Settings()