# =============================================================================
# SRP: MathEngine - ÚNICA responsabilidad: realizar operaciones aritméticas
# Alta Cohesión: todos los métodos ejecutan cálculos matemáticos básicos
# =============================================================================


class MathEngine:
    """
    Motor de cálculos aritméticos básicos.

    Responsabilidad única: ejecutar operaciones matemáticas (+, -, *, /).
    Alta cohesión: todos los métodos son cálculos aritméticos puros.

    Razón para cambiar: solo si se agregan o modifican operaciones básicas.
    """

    @staticmethod
    def add(a: float, b: float) -> float:
        """Suma dos números."""
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Resta dos números."""
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiplica dos números."""
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        """Divide dos números. El llamador debe validar que b != 0."""
        return a / b

    def calculate(self, operator: str, a: float, b: float):
        """
        Ejecuta la operación indicada por el operador.
        Retorna el resultado numérico o None si el operador no es válido.
        """
        operations = {
            "+": self.add,
            "-": self.subtract,
            "*": self.multiply,
            "/": self.divide,
        }

        operation = operations.get(operator)
        if operation is None:
            return None

        return operation(a, b)
