import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase

# 1. Recuperar la URL de la BD desde el entorno de Docker
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://saas_admin:secure_password_2026@postgres:5432/saas_db"
)

# 2. Crear el Motor Asíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_size=10,
    max_overflow=20
)

# 3. Fabrica de Sesiones Asíncronas
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 4. Base Declarativa para los Modelos
class Base(DeclarativeBase):
    pass

# 5. Inyección de Dependencia para los Endpoints de FastAPI
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()