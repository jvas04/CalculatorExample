# =============================================================================
# SRP: MemoryManager - ÚNICA responsabilidad: gestionar la memoria numérica
# Alta Cohesión: todos los métodos operan sobre el valor almacenado en memoria
# =============================================================================


class MemoryManager:
    """
    Gestiona la memoria numérica de la calculadora (M+, M-, MR, MC).

    Responsabilidad única: almacenar y operar sobre un valor en memoria.
    Alta cohesión: todos los métodos manipulan el mismo dato de memoria.

    Razón para cambiar: solo si cambian las operaciones de memoria.
    """

    def __init__(self):
        self._memory: float = 0

    def clear(self) -> None:
        """Limpia la memoria (MC)."""
        self._memory = 0

    def recall(self) -> float:
        """Retorna el valor almacenado en memoria (MR)."""
        return self._memory

    def add(self, value: float) -> None:
        """Suma un valor a la memoria (M+)."""
        self._memory += value

    def subtract(self, value: float) -> None:
        """Resta un valor de la memoria (M-)."""
        self._memory -= value

    def has_value(self) -> bool:
        """Indica si hay un valor no-cero almacenado en memoria."""
        return self._memory != 0
