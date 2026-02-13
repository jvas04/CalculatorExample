# =============================================================================
# SRP: ScientificOperations - ÚNICA responsabilidad: operaciones científicas
# Alta Cohesión: todos los métodos son cálculos científicos/avanzados
# =============================================================================

import math


class ScientificOperations:
    """
    Realiza operaciones matemáticas científicas y avanzadas.

    Responsabilidad única: ejecutar cálculos científicos (√, x², %, π).
    Alta cohesión: todos los métodos son operaciones matemáticas avanzadas.

    Razón para cambiar: solo si se agregan o modifican operaciones científicas.
    """

    @staticmethod
    def square_root(number: float) -> float:
        """Calcula la raíz cuadrada. El llamador debe validar que number >= 0."""
        return math.sqrt(number)

    @staticmethod
    def square(number: float) -> float:
        """Eleva un número al cuadrado."""
        return number ** 2

    @staticmethod
    def percentage(number: float) -> float:
        """Convierte un número a su valor porcentual (divide entre 100)."""
        return number / 100

    @staticmethod
    def negate(number: float) -> float:
        """Cambia el signo de un número."""
        return -number

    @staticmethod
    def get_pi() -> float:
        """Retorna el valor de PI."""
        return math.pi
