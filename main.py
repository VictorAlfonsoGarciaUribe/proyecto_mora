from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from sqlalchemy import text
from schemas.produccion import ReporteProduccion
from workers.tasks import procesar_reporte_pesado
from core.database import engine, Base
import core.models  # Registra los modelos (Tenant, User, Product) en la metadata del ORM

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Evento de arranque (Startup): Inicialización de BD
    async with engine.begin() as conn:
        # 1. Habilitar la extensión pgvector en PostgreSQL para embeddings de IA
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        # 2. Crear tablas si no existen en la base de datos
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Evento de apagado (Shutdown): Liberar pool de conexiones
    await engine.dispose()

app = FastAPI(
    title="MORA API - Comercio Agéntico SaaS",
    version="0.5.0",
    description="Motor de Orquestación y Resolución Asíncrona con Persistencia Asíncrona y Vectorial",
    lifespan=lifespan
)

@app.get("/")
def health_check():
    """Endpoint de verificación de estado del sistema."""
    return {"status": "activo", "version": "0.5.0", "database": "connected"}

@app.post("/api/v1/produccion", status_code=status.HTTP_202_ACCEPTED)
def registrar_produccion(payload: ReporteProduccion):
    """
    Recibe el reporte, lo valida estrictamente con Pydantic, 
    lo encola en Redis mediante Celery y responde inmediatamente (202 Accepted).
    """
    datos_dict = payload.model_dump()
    tarea = procesar_reporte_pesado.delay(reporte_id=999, datos=datos_dict)
    
    return {
        "mensaje": "Reporte recibido y encolado exitosamente para procesamiento asíncrono",
        "task_id": tarea.id,
        "estado": "en_cola"
    }