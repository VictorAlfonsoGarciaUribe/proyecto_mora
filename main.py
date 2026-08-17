from fastapi import FastAPI, status
from schemas.produccion import ReporteProduccion
from workers.tasks import procesar_reporte_pesado

app = FastAPI(
    title="MORA API",
    version="0.2.0",
    description="Motor de Orquestación y Resolución Asíncrona - Módulo de Concurrencia"
)

@app.get("/")
def health_check():
    """Endpoint de verificación de estado del sistema."""
    return {"status": "activo", "version": "0.2.0"}

@app.post("/api/v1/produccion", status_code=status.HTTP_202_ACCEPTED)
def registrar_produccion(payload: ReporteProduccion):
    """
    Recibe el reporte, lo valida estrictamente con Pydantic, 
    lo encola en Redis mediante Celery y responde inmediatamente (202 Accepted).
    """
    # Convertimos el modelo Pydantic a un diccionario plano de Python
    datos_dict = payload.model_dump()
    
    # Enviamos la tarea a la cola de Celery en segundo plano (.delay)
    tarea = procesar_reporte_pesado.delay(reporte_id=999, datos=datos_dict)
    
    return {
        "mensaje": "Reporte recibido y encolado exitosamente para procesamiento asíncrono",
        "task_id": tarea.id,
        "estado": "en_cola"
    }