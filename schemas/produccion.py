from pydantic import BaseModel, Field, field_validator
from typing import Literal, Any
import re

class ReporteProduccion(BaseModel):
    """
    Esquema de validación para reportes de producción.
    Garantiza la integridad estructural y la sanitización de datos antes de la persistencia.
    """
    operador_id: int = Field(
        ..., 
        ge=100, 
        le=9999, 
        description="ID corporativo del operador."
    )
    piezas_producidas: int = Field(
        ..., 
        ge=0, 
        le=5000, 
        description="Volumen de producción registrado."
    )
    nivel_riesgo: Literal["bajo", "medio", "alto"]
    
    transaction_code: str = Field(
        ..., 
        description="Identificador único de trazabilidad bajo el estándar CORP-{DEPT}-{HASH}"
    )

    @field_validator("transaction_code", mode="before")
    @classmethod
    def sanitizar_y_validar_codigo(cls, valor: Any) -> str:
        if not isinstance(valor, str):
            raise TypeError("El código de transacción debe ser de tipo texto.")
        
        codigo_limpio = valor.strip().upper()
        
        # Validar estructura mediante expresión regular estricta
        if not re.match(r"^CORP-([A-Z]{3})-(\d{4})$", codigo_limpio):
            raise ValueError(f"Formato inválido: '{valor}'. Estructura requerida: CORP-XXX-0000.")
        
        # Extraer y validar el centro de costo contra las reglas de negocio
        departamento = codigo_limpio.split("-")[1]
        departamentos_validos = {"LOG", "OPS", "TEC", "SAF"}
        
        if departamento not in departamentos_validos:
            raise ValueError(f"Centro de costo '{departamento}' no autorizado.")
            
        return codigo_limpio