import pytest
from pydantic import ValidationError
from schemas.produccion import ReporteProduccion


def test_reporte_produccion_exitoso_con_sanitizacion():
    """Verifica que Pydantic limpie espacios, pase a mayúsculas y valide correctamente."""
    payload = ReporteProduccion(
        operador_id=1520,
        piezas_producidas=450,
        nivel_riesgo="bajo",
        transaction_code="  corp-log-1052  "
    )
    
    assert payload.transaction_code == "CORP-LOG-1052"
    assert payload.operador_id == 1520


def test_departamento_no_autorizado_falla():
    """Verifica que un centro de costo no autorizado arroje un error de validación."""
    with pytest.raises(ValidationError) as exc_info:
        ReporteProduccion(
            operador_id=1520,
            piezas_producidas=100,
            nivel_riesgo="alto",
            transaction_code="CORP-MKT-9999"
        )
        
    assert "Centro de costo" in str(exc_info.value)


def test_estructura_transaction_code_rota_falla():
    """Verifica que un formato inválido active la excepción del patrón regex."""
    with pytest.raises(ValidationError) as exc_info:
        ReporteProduccion(
            operador_id=1520,
            piezas_producidas=100,
            nivel_riesgo="medio",
            transaction_code="INVALIDO-123"
        )
        
    assert "Formato inválido" in str(exc_info.value)