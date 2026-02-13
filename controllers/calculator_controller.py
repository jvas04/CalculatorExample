# =============================================================================
# SRP: CalculatorController - ÚNICA responsabilidad: coordinar componentes
# Alta Cohesión: todos los métodos orquestan la comunicación entre capas
# =============================================================================
#
# Este controlador es el ORQUESTADOR que conecta la Vista con los Modelos.
# No contiene lógica de negocio (eso está en MathEngine, ScientificOperations,
# etc.) ni lógica de UI (eso está en CalculatorView). Solo COORDINA.
# =============================================================================

from tkinter import messagebox, filedialog

from utils.theme_manager import ThemeManager
from utils.number_formatter import NumberFormatter
from utils.input_validator import InputValidator
from services.error_logger import ErrorLogger
from models.math_engine import MathEngine
from models.scientific_operations import ScientificOperations
from models.memory_manager import MemoryManager
from models.history_manager import HistoryManager
from views.history_view import HistoryView
from services.file_manager import FileManager
from models.statistics_reporter import StatisticsReporter


class CalculatorController:
    """
    Controlador que coordina la comunicación entre la Vista y los Modelos.

    Responsabilidad única: orquestar el flujo de datos entre componentes.
    Alta cohesión: todos los métodos coordinan interacciones entre capas.

    Razón para cambiar: solo si cambia el flujo de coordinación entre capas.

    Cada componente inyectado tiene su propia responsabilidad única:
        - ThemeManager:          gestión de temas visuales
        - NumberFormatter:       formateo de números
        - InputValidator:        validación de entrada
        - ErrorLogger:           registro de errores
        - MathEngine:            operaciones aritméticas
        - ScientificOperations:  operaciones científicas
        - MemoryManager:         memoria de la calculadora
        - HistoryManager:        historial de operaciones
        - FileManager:           persistencia en archivos
        - StatisticsReporter:    estadísticas de uso
    """

    def __init__(self, view):
        # Inyección de dependencias — cada componente con SU responsabilidad
        self.view = view
        self.theme = ThemeManager()
        self.formatter = NumberFormatter()
        self.validator = InputValidator()
        self.logger = ErrorLogger()
        self.math = MathEngine()
        self.scientific = ScientificOperations()
        self.memory = MemoryManager()
        self.history = HistoryManager()
        self.file_mgr = FileManager()
        self.stats = StatisticsReporter()

        # Estado del flujo de entrada (solo datos de coordinación)
        self.current_input = ""
        self.first_number = None
        self.operator = None
        self.waiting_for_second = False

    # =========================================================================
    #  Inicialización de la interfaz con callbacks
    # =========================================================================

    def initialize(self) -> None:
        """Construye toda la UI conectando callbacks del controlador."""
        colors = self.theme.get_colors()

        self.view.setup_window()
        self.view.build_top_bar(on_toggle_theme=self.on_toggle_theme)
        self.view.build_display()

        self.view.build_memory_buttons([
            ("MC", self.on_memory_clear),
            ("MR", self.on_memory_recall),
            ("M+", self.on_memory_add),
            ("M-", self.on_memory_subtract),
            ("📋 Hist", self.on_show_history),
            ("💾 Guardar", self.on_save_history),
        ])

        self.view.build_scientific_buttons([
            ("√", self.on_sqrt),
            ("x²", self.on_square),
            ("%", self.on_percentage),
            ("±", self.on_toggle_sign),
            ("π", self.on_insert_pi),
        ])

        self.view.build_keypad(
            button_layout=[
                ("C", 0, 0, colors["bg_clear"], colors["fg_clear"], self.on_clear),
                ("⌫", 0, 1, colors["bg_clear"], colors["fg_clear"], self.on_backspace),
                ("(", 0, 2, "#233554", "#a0cfe4", lambda: self.on_digit("(")),
                ("÷", 0, 3, colors["bg_operator"], "#fff", lambda: self.on_operator("/")),
                ("7", 1, 0, colors["bg_button"], "#fff", lambda: self.on_digit("7")),
                ("8", 1, 1, colors["bg_button"], "#fff", lambda: self.on_digit("8")),
                ("9", 1, 2, colors["bg_button"], "#fff", lambda: self.on_digit("9")),
                ("×", 1, 3, colors["bg_operator"], "#fff", lambda: self.on_operator("*")),
                ("4", 2, 0, colors["bg_button"], "#fff", lambda: self.on_digit("4")),
                ("5", 2, 1, colors["bg_button"], "#fff", lambda: self.on_digit("5")),
                ("6", 2, 2, colors["bg_button"], "#fff", lambda: self.on_digit("6")),
                ("−", 2, 3, colors["bg_operator"], "#fff", lambda: self.on_operator("-")),
                ("1", 3, 0, colors["bg_button"], "#fff", lambda: self.on_digit("1")),
                ("2", 3, 1, colors["bg_button"], "#fff", lambda: self.on_digit("2")),
                ("3", 3, 2, colors["bg_button"], "#fff", lambda: self.on_digit("3")),
                ("+", 3, 3, colors["bg_operator"], "#fff", lambda: self.on_operator("+")),
                ("0", 4, 0, colors["bg_button"], "#fff", lambda: self.on_digit("0")),
                ("00", 4, 1, colors["bg_button"], "#fff", lambda: self.on_digit("00")),
                (".", 4, 2, colors["bg_button"], "#fff", lambda: self.on_digit(".")),
                ("=", 4, 3, colors["bg_equal"], "#fff", self.on_equals),
            ],
            get_hover_color=self.theme.get_hover_color,
        )

        self.view.build_stats_bar()
        self.view.bind_keyboard(self.on_keypress)

    # =========================================================================
    #  Handlers de entrada numérica
    # =========================================================================

    def on_digit(self, char: str) -> None:
        """Maneja la entrada de un dígito o punto decimal."""
        if self.waiting_for_second:
            self.current_input = ""
            self.waiting_for_second = False

        if char == "." and not self.validator.can_add_decimal(self.current_input):
            return

        self.current_input += char
        self.view.update_display(self.current_input)

    # =========================================================================
    #  Handlers de operadores
    # =========================================================================

    def on_operator(self, op: str) -> None:
        """Maneja la selección de un operador aritmético."""
        if self.current_input == "" and self.first_number is None:
            return

        if self.current_input != "":
            if self.first_number is not None and self.operator is not None:
                self.on_equals()

            num = self.validator.parse_number(self.current_input)
            if num is None:
                self.view.update_display("Error")
                return
            self.first_number = num

        self.operator = op
        symbol = self.formatter.get_operator_symbol(op)
        self.view.update_history_text(
            f"{self.formatter.format(self.first_number)} {symbol}"
        )
        self.current_input = ""
        self.waiting_for_second = False

    def on_equals(self) -> None:
        """Ejecuta el cálculo con el operador y números actuales."""
        if self.operator is None or self.first_number is None:
            return

        second = self.validator.parse_number(self.current_input)
        if second is None:
            self.view.update_display("Error")
            return

        # Validar división por cero (el Validator valida, el Controller decide)
        if self.operator == "/" and self.validator.is_division_by_zero(second):
            self.view.update_display("Error")
            self.view.update_history_text("Error: División por cero")
            messagebox.showerror("Error", "No se puede dividir entre cero.")
            self.logger.log("División por cero")
            self._reset_operation()
            return

        # Delegar el cálculo al MathEngine
        result = self.math.calculate(self.operator, self.first_number, second)

        # Registrar estadística (StatisticsReporter se encarga)
        self.stats.record_operation(self.operator)

        # Formatear resultado (NumberFormatter se encarga)
        symbol = self.formatter.get_operator_symbol(self.operator)
        formatted = self.formatter.format(result)

        # Actualizar vista
        self.view.update_display(formatted)
        self.view.update_history_text(
            f"{self.formatter.format(self.first_number)} {symbol} "
            f"{self.formatter.format(second)} ="
        )
        self.view.update_stats_text(
            f"Operaciones realizadas: {self.stats.get_total()}"
        )

        # Registrar en historial (HistoryManager se encarga)
        self.history.add_record(
            f"{self.first_number} {symbol} {second}", result
        )

        # Preparar para siguiente operación
        self.first_number = result
        self.current_input = formatted
        self.operator = None
        self.waiting_for_second = True

    # =========================================================================
    #  Handlers de operaciones científicas
    # =========================================================================

    def on_sqrt(self) -> None:
        """Coordina la operación de raíz cuadrada."""
        num = self._get_validated_display_number()
        if num is None:
            return

        if self.validator.is_negative(num):
            self.view.update_display("Error")
            messagebox.showerror(
                "Error", "No se puede calcular raíz de un número negativo."
            )
            return

        result = self.scientific.square_root(num)
        self._apply_scientific_result(result, f"√({self.formatter.format(num)})")

    def on_square(self) -> None:
        """Coordina la operación de elevar al cuadrado."""
        num = self._get_validated_display_number()
        if num is None:
            return

        result = self.scientific.square(num)
        self._apply_scientific_result(
            result, f"({self.formatter.format(num)})²"
        )

    def on_percentage(self) -> None:
        """Coordina la operación de porcentaje."""
        num = self._get_validated_display_number()
        if num is None:
            return

        result = self.scientific.percentage(num)
        formatted = self.formatter.format(result)
        self.view.update_display(formatted)
        self.view.update_history_text(f"{self.formatter.format(num)}%")
        self.current_input = formatted

    def on_toggle_sign(self) -> None:
        """Coordina el cambio de signo."""
        num = self._get_validated_display_number()
        if num is None:
            return

        result = self.scientific.negate(num)
        formatted = self.formatter.format(result)
        self.view.update_display(formatted)
        self.current_input = formatted

    def on_insert_pi(self) -> None:
        """Inserta el valor de PI."""
        pi = self.scientific.get_pi()
        self.current_input = str(pi)
        self.view.update_display(self.formatter.format(pi))

    # =========================================================================
    #  Handlers de memoria
    # =========================================================================

    def on_memory_clear(self) -> None:
        self.memory.clear()
        messagebox.showinfo("Memoria", "Memoria limpiada.")

    def on_memory_recall(self) -> None:
        value = self.memory.recall()
        self.current_input = self.formatter.format(value)
        self.view.update_display(self.current_input)

    def on_memory_add(self) -> None:
        num = self.validator.parse_number(self.view.get_display_value())
        if num is not None:
            self.memory.add(num)

    def on_memory_subtract(self) -> None:
        num = self.validator.parse_number(self.view.get_display_value())
        if num is not None:
            self.memory.subtract(num)

    # =========================================================================
    #  Handlers de historial y persistencia
    # =========================================================================

    def on_show_history(self) -> None:
        """Abre la ventana de historial delegando a HistoryView."""
        colors = self.theme.get_colors()
        history_view = HistoryView(self.view.window, colors)
        history_view.show(
            records=self.history.get_records_reversed(),
            format_number=self.formatter.format,
            on_clear=self._clear_all_data,
            on_statistics=self.on_show_statistics,
        )

    def on_save_history(self) -> None:
        """Coordina el guardado del historial en archivo."""
        if self.history.is_empty():
            messagebox.showinfo("Guardar", "No hay historial para guardar.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
            title="Guardar historial",
        )

        if not filepath:
            return

        try:
            self.file_mgr.save(
                filepath,
                self.history.get_all_records(),
                self.stats.get_stats_dict(),
            )
            messagebox.showinfo("Guardado", f"Historial guardado en:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")
            self.logger.log(f"Error al guardar archivo: {e}")

    def on_show_statistics(self) -> None:
        """Muestra el reporte de estadísticas."""
        results = self.history.get_all_results() if not self.history.is_empty() else None
        report = self.stats.generate_report(results)
        messagebox.showinfo("Estadísticas", report)

    # =========================================================================
    #  Handlers de tema y limpieza
    # =========================================================================

    def on_toggle_theme(self) -> None:
        """Coordina el cambio de tema visual."""
        new_colors = self.theme.toggle_theme()
        icon = self.theme.get_theme_icon()
        self.view.update_theme(new_colors, icon)

    def on_clear(self) -> None:
        """Limpia el display y el estado de operación actual."""
        self.current_input = ""
        self.first_number = None
        self.operator = None
        self.waiting_for_second = False
        self.view.update_display("0")
        self.view.update_history_text("")

    def on_backspace(self) -> None:
        """Borra el último carácter del input."""
        self.current_input = self.current_input[:-1]
        self.view.update_display(
            self.current_input if self.current_input else "0"
        )

    # =========================================================================
    #  Handler de teclado físico
    # =========================================================================

    def on_keypress(self, event) -> None:
        """Mapea teclas del teclado físico a acciones de la calculadora."""
        key = event.char
        keysym = event.keysym

        key_actions = {
            "0": lambda: self.on_digit("0"),
            "1": lambda: self.on_digit("1"),
            "2": lambda: self.on_digit("2"),
            "3": lambda: self.on_digit("3"),
            "4": lambda: self.on_digit("4"),
            "5": lambda: self.on_digit("5"),
            "6": lambda: self.on_digit("6"),
            "7": lambda: self.on_digit("7"),
            "8": lambda: self.on_digit("8"),
            "9": lambda: self.on_digit("9"),
            ".": lambda: self.on_digit("."),
            "+": lambda: self.on_operator("+"),
            "-": lambda: self.on_operator("-"),
            "*": lambda: self.on_operator("*"),
            "/": lambda: self.on_operator("/"),
            "=": self.on_equals,
        }

        keysym_actions = {
            "Return": self.on_equals,
            "BackSpace": self.on_backspace,
            "Escape": self.on_clear,
            "Delete": self.on_clear,
        }

        action = key_actions.get(key) or keysym_actions.get(keysym)
        if action:
            action()

    # =========================================================================
    #  Métodos internos de coordinación
    # =========================================================================

    def _get_validated_display_number(self):
        """Obtiene y valida el número del display. Retorna float o None."""
        display_value = self.view.get_display_value()
        if not self.validator.is_valid_display(display_value):
            messagebox.showwarning(
                "Entrada inválida", "Por favor ingrese un número válido."
            )
            return None

        num = self.validator.parse_number(display_value)
        if num is None:
            self.view.update_display("Error")
            return None

        return num

    def _apply_scientific_result(self, result: float, expression: str) -> None:
        """Aplica el resultado de una operación científica a la vista y al historial."""
        formatted = self.formatter.format(result)
        self.view.update_display(formatted)
        self.view.update_history_text(expression)
        self.history.add_record(expression, result)
        self.current_input = formatted
        self.stats.record_scientific()
        self.view.update_stats_text(
            f"Operaciones realizadas: {self.stats.get_total()}"
        )

    def _reset_operation(self) -> None:
        """Reinicia el estado de la operación actual."""
        self.current_input = ""
        self.operator = None
        self.first_number = None

    def _clear_all_data(self) -> None:
        """Limpia historial y estadísticas."""
        self.history.clear()
        self.stats.reset()
        self.view.update_stats_text("Operaciones realizadas: 0")
        messagebox.showinfo("Historial", "Historial limpiado correctamente.")
