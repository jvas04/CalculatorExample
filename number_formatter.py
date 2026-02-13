# =============================================================================
# SRP: NumberFormatter - ÚNICA responsabilidad: formatear números para mostrar
# Alta Cohesión: todos los métodos se relacionan con el formateo de números
# =============================================================================


class NumberFormatter:
    """
    Formatea números para su presentación en el display.

    Responsabilidad única: convertir valores numéricos a strings legibles.
    Alta cohesión: todos los métodos transforman datos numéricos a texto.

    Razón para cambiar: solo si cambian las reglas de formato numérico.
    """

    @staticmethod
    def format(number) -> str:
        """Formatea un número para mostrar en el display."""
        if number is None:
            return "Error"
        if isinstance(number, float) and number == int(number):
            return str(int(number))
        if isinstance(number, float):
            return f"{number:.8g}"
        return str(number)

    @staticmethod
    def get_operator_symbol(operator: str) -> str:
        """Convierte un operador interno a su símbolo visual."""
        symbols = {"+": "+", "-": "−", "*": "×", "/": "÷"}
        return symbols.get(operator, operator)
