# =============================================================================
# SRP: HistoryManager - ÚNICA responsabilidad: gestionar el historial
# Alta Cohesión: todos los métodos operan sobre la lista de registros
# =============================================================================

from datetime import datetime


class HistoryManager:
    """
    Gestiona el historial de operaciones realizadas.

    Responsabilidad única: agregar, consultar y limpiar registros del historial.
    Alta cohesión: todos los métodos operan sobre la colección de registros.

    Razón para cambiar: solo si cambia la estructura o gestión del historial.
    """

    def __init__(self):
        self._records: list[dict] = []

    def add_record(self, expression: str, result: float) -> None:
        """Agrega un nuevo registro al historial con timestamp automático."""
        record = {
            "expression": expression,
            "result": result,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        }
        self._records.append(record)

    def get_all_records(self) -> list[dict]:
        """Retorna todos los registros del historial."""
        return self._records.copy()

    def get_records_reversed(self) -> list[dict]:
        """Retorna los registros en orden inverso (más recientes primero)."""
        return list(reversed(self._records))

    def clear(self) -> None:
        """Limpia todo el historial."""
        self._records.clear()

    def get_all_results(self) -> list[float]:
        """Retorna solo los resultados numéricos de todos los registros."""
        return [r["result"] for r in self._records]

    def is_empty(self) -> bool:
        """Indica si el historial está vacío."""
        return len(self._records) == 0

    def count(self) -> int:
        """Retorna la cantidad de registros en el historial."""
        return len(self._records)
