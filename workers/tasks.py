"""
Módulo de tareas asíncronas ejecutadas en segundo plano mediante Celery.
Orquesta el pipeline de procesamiento analítico y de IA utilizando grafos de estado.
"""

from typing import Dict, Any
from core.celery_app import celery_app
from workers.agent_graph import mora_graph


@celery_app.task(name="tasks.procesar_reporte_pesado")
def procesar_reporte_pesado(reporte_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ejecuta el pipeline asíncrono en segundo plano de manera tolerante a fallos.
    Toma los datos validados de la API y los procesa a través del grafo de estados de LangGraph.
    """
    print(f"[*] Iniciando ejecución asíncrona en el worker para el reporte ID: {reporte_id}...")
    
    # Estado inicial estricto que alimenta el grafo de LangGraph
    estado_inicial = {
        "reporte_id": reporte_id,
        "datos_entrada": datos,
        "analisis_ia": "",
        "intentos": 0,
        "estado_proceso": "iniciado"
    }
    
    try:
        # Invocación síncrona del grafo de estados dentro del worker de Celery
        resultado_grafo = mora_graph.invoke(estado_inicial)
        
        resultado_final = {
            "reporte_id": reporte_id,
            "estado": resultado_grafo.get("estado_proceso", "completado"),
            "dictamen_ia": resultado_grafo.get("analisis_ia", "Sin respuesta generada"),
            "intentos_ejecucion": resultado_grafo.get("intentos", 1),
            "datos_normalizados": datos
        }
        
        print(f"[*] ¡Procesamiento cognitivo finalizado con éxito para el reporte ID: {reporte_id}!")
        return resultado_final
        
    except Exception as exc:
        print(f"[!] Error crítico en el pipeline de IA para el reporte ID {reporte_id}: {str(exc)}")
        # Relanzamos la excepción para que Celery registre el fallo en la infraestructura de colas
        raise exc