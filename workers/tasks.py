import time
from core.celery_app import celery_app

@celery_app.task(name="tasks.procesar_reporte_pesado")
def procesar_reporte_pesado(reporte_id: int, datos: dict):
    """
    Simula una tarea pesada de procesamiento (como llamadas a un LLM, análisis de datos o OCR)
    que toma varios segundos y no debe bloquear la API web.
    """
    print(f"[*] Iniciando procesamiento en segundo plano para el reporte ID: {reporte_id}...")
    
    # Simulamos un retraso de 5 segundos de procesamiento intensivo (I/O Bound)
    time.sleep(5)
    
    # Aquí iría la lógica real de procesamiento con IA o bases de datos
    resultado_simulado = {
        "reporte_id": reporte_id,
        "estado": "procesado_exitosamente",
        "datos_normalizados": datos,
        "metricas": {"tokens_usados": 150, "confianza": 0.98}
    }
    
    print(f"[*] ¡Procesamiento finalizado para el reporte ID: {reporte_id}!")
    return resultado_simulado