# =============================================================================
# SRP: ThemeManager - ÚNICA responsabilidad: gestionar colores y temas visuales
# Alta Cohesión: todos los métodos están relacionados con la apariencia visual
# =============================================================================


class ThemeManager:
    """
    Gestiona los temas visuales de la aplicación.

    Responsabilidad única: definir y cambiar paletas de colores.
    Alta cohesión: todos los métodos se relacionan con la apariencia visual.

    Razón para cambiar: solo si cambian los requisitos visuales/de tema.
    """

    DARK_THEME = {
        "bg_main": "#1a1a2e",
        "bg_display": "#16213e",
        "bg_button": "#0f3460",
        "bg_button_hover": "#1a5276",
        "bg_operator": "#e94560",
        "bg_operator_hover": "#c0392b",
        "bg_equal": "#00b894",
        "bg_equal_hover": "#00a381",
        "bg_clear": "#fdcb6e",
        "bg_clear_hover": "#f0b842",
        "bg_scientific": "#6c5ce7",
        "bg_scientific_hover": "#5b4cdb",
        "bg_memory": "#233554",
        "bg_memory_hover": "#2c4a6e",
        "fg_display": "#ffffff",
        "fg_button": "#ffffff",
        "fg_history": "#a0a0a0",
        "fg_clear": "#2d3436",
        "fg_memory": "#a0cfe4",
        "fg_title": "#e94560",
        "fg_stats": "#636e72",
        "border": "#233554",
    }

    LIGHT_THEME = {
        "bg_main": "#f5f6fa",
        "bg_display": "#ffffff",
        "bg_button": "#dfe6e9",
        "bg_button_hover": "#b2bec3",
        "bg_operator": "#e94560",
        "bg_operator_hover": "#c0392b",
        "bg_equal": "#00b894",
        "bg_equal_hover": "#00a381",
        "bg_clear": "#fdcb6e",
        "bg_clear_hover": "#f0b842",
        "bg_scientific": "#6c5ce7",
        "bg_scientific_hover": "#5b4cdb",
        "bg_memory": "#b2bec3",
        "bg_memory_hover": "#636e72",
        "fg_display": "#2d3436",
        "fg_button": "#2d3436",
        "fg_history": "#636e72",
        "fg_clear": "#2d3436",
        "fg_memory": "#2d3436",
        "fg_title": "#e94560",
        "fg_stats": "#636e72",
        "border": "#b2bec3",
    }

    def __init__(self):
        self.is_dark_mode = True
        self._current_theme = self.DARK_THEME.copy()

    def get_colors(self) -> dict:
        """Retorna la paleta de colores del tema actual."""
        return self._current_theme

    def toggle_theme(self) -> dict:
        """Alterna entre tema oscuro y claro. Retorna la nueva paleta."""
        self.is_dark_mode = not self.is_dark_mode
        self._current_theme = (
            self.DARK_THEME.copy() if self.is_dark_mode else self.LIGHT_THEME.copy()
        )
        return self._current_theme

    def get_hover_color(self, base_color: str) -> str:
        """Dado un color base de botón, retorna su color hover correspondiente."""
        hover_map = {
            self._current_theme["bg_button"]: self._current_theme["bg_button_hover"],
            self._current_theme["bg_operator"]: self._current_theme["bg_operator_hover"],
            self._current_theme["bg_equal"]: self._current_theme["bg_equal_hover"],
            self._current_theme["bg_clear"]: self._current_theme["bg_clear_hover"],
            self._current_theme["bg_scientific"]: self._current_theme["bg_scientific_hover"],
        }
        return hover_map.get(base_color, base_color)

    def get_theme_icon(self) -> str:
        """Retorna el ícono del botón de tema según el modo actual."""
        return "☀️" if self.is_dark_mode else "🌙"
