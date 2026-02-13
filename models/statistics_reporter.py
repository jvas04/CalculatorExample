# =============================================================================
# SRP: StatisticsReporter - ÚNICA responsabilidad: generar estadísticas
# Alta Cohesión: todos los métodos se relacionan con cálculo y reporte de stats
# =============================================================================


class StatisticsReporter:
    """
    Genera y gestiona estadísticas de uso de la calculadora.

    Responsabilidad única: contar operaciones y generar reportes estadísticos.
    Alta cohesión: todos los métodos calculan o reportan métricas de uso.

    Razón para cambiar: solo si cambian las métricas o el formato del reporte.
    """

    def __init__(self):
        self._stats = {"sum": 0, "sub": 0, "mul": 0, "div": 0, "sci": 0}

    def record_operation(self, operator: str) -> None:
        """Registra que se realizó una operación según el operador."""
        operator_map = {
            "+": "sum",
            "-": "sub",
            "*": "mul",
            "/": "div",
        }
        key = operator_map.get(operator)
        if key:
            self._stats[key] += 1

    def record_scientific(self) -> None:
        """Registra que se realizó una operación científica."""
        self._stats["sci"] += 1

    def get_total(self) -> int:
        """Retorna el total de operaciones realizadas."""
        return sum(self._stats.values())

    def get_stats_dict(self) -> dict:
        """Retorna una copia del diccionario de estadísticas."""
        return self._stats.copy()

    def generate_report(self, results: list[float] = None) -> str:
        """Genera un reporte de estadísticas en texto formateado."""
        total = self.get_total()
        msg = (
            f"📊 Estadísticas de Uso\n"
            f"{'─' * 30}\n"
            f"  Sumas:                {self._stats['sum']}\n"
            f"  Restas:               {self._stats['sub']}\n"
            f"  Multiplicaciones:  {self._stats['mul']}\n"
            f"  Divisiones:           {self._stats['div']}\n"
            f"  Científicas:          {self._stats['sci']}\n"
            f"{'─' * 30}\n"
            f"  TOTAL:                {total}\n"
        )

        if results:
            msg += (
                f"\n📈 Análisis de Resultados\n"
                f"{'─' * 30}\n"
                f"  Máximo:  {max(results)}\n"
                f"  Mínimo:   {min(results)}\n"
                f"  Promedio: {sum(results) / len(results):.4f}\n"
            )

        return msg

    def reset(self) -> None:
        """Reinicia todas las estadísticas a cero."""
        self._stats = {"sum": 0, "sub": 0, "mul": 0, "div": 0, "sci": 0}
