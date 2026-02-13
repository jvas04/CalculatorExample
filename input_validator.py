# =============================================================================
# SRP: InputValidator - ÚNICA responsabilidad: validar entrada del usuario
# Alta Cohesión: todos los métodos se relacionan con validación de datos
# =============================================================================


class InputValidator:
    """
    Valida la entrada del usuario antes de procesarla.

    Responsabilidad única: determinar si un dato de entrada es válido.
    Alta cohesión: todos los métodos verifican y validan datos.

    Razón para cambiar: solo si cambian las reglas de validación.
    """

    @staticmethod
    def parse_number(value: str):
        """
        Intenta convertir un string a número.
        Retorna el float si es válido, None si no lo es.
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def is_valid_display(value: str) -> bool:
        """Verifica que el valor del display sea procesable (no vacío ni error)."""
        return value not in ("", "Error")

    @staticmethod
    def can_add_decimal(current_input: str) -> bool:
        """Verifica si se puede agregar un punto decimal al input actual."""
        return "." not in current_input

    @staticmethod
    def is_division_by_zero(divisor: float) -> bool:
        """Verifica si el divisor es cero."""
        return divisor == 0

    @staticmethod
    def is_negative(value: float) -> bool:
        """Verifica si un número es negativo (para validar raíz cuadrada)."""
        return value < 0
