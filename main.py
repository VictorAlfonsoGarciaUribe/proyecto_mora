from contextlib import asynccontextmanager
from fastapi import FastAPI, status

from schemas.produccion import ReporteProduccion
from workers.tasks import procesar_reporte_pesado
from core.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Evento de arranque (Startup): Limpio y pasivo
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
    lo encola en Redis mediante Celery y responde inmediatamente.
    """
    datos_dict = payload.model_dump()
    tarea = procesar_reporte_pesado.delay(reporte_id=999, datos=datos_dict)
    
    return {
        "mensaje": "Reporte recibido y encolado exitosamente para procesamiento asíncrono",
        "task_id": tarea.id,
        "estado": "en_cola"
    }