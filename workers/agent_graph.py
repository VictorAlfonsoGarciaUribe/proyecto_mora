from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import settings

class State(TypedDict):
    reporte_id: int
    datos_entrada: dict
    analisis_ia: str
    intentos: int
    estado_proceso: str

# Inicializamos el modelo Gemini con control determinista (temperatura baja)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.1,
    google_api_key=settings.GOOGLE_API_KEY
)

def nodo_analisis_inteligente(state: State) -> State:
    """Nodo del grafo que procesa inteligentemente el reporte mediante Gemini."""
    print(f"[*] Ejecutando nodo de IA (Gemini) para el reporte ID: {state['reporte_id']}")
    
    datos = state["datos_entrada"]
    prompt = (
        f"Analiza el siguiente reporte operativo de producción y genera un dictamen ejecutivo en una línea: "
        f"Operador: {datos.get('operador_id')}, "
        f"Piezas: {datos.get('piezas_producidas')}, "
        f"Riesgo: {datos.get('nivel_riesgo')}, "
        f"Código: {datos.get('transaction_code')}"
    )
    
    try:
        respuesta = llm.invoke(prompt)
        state["analisis_ia"] = respuesta.content
        state["estado_proceso"] = "completado"
    except Exception as e:
        state["analisis_ia"] = f"Error en inferencia: {str(e)}"
        state["estado_proceso"] = "fallido"
        
    state["intentos"] += 1
    return state

def decidir_siguiente_paso(state: State) -> str:
    """Enrutador condicional para reintentos en caso de falla del modelo."""
    if state["estado_proceso"] == "fallido" and state["intentos"] < 2:
        return "reintentar"
    return "finalizar"

# Construcción del Grafo de Estados de LangGraph
workflow = StateGraph(State)

workflow.add_node("analizar_reporte", nodo_analisis_inteligente)
workflow.set_entry_point("analizar_reporte")

workflow.add_conditional_edges(
    "analizar_reporte",
    decidir_siguiente_paso,
    {
        "reintentar": "analizar_reporte",
        "finalizar": END
    }
)

mora_graph = workflow.compile()