import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import json
import math
import os


class Calculator:
    
    def __init__(self):
        # =====================================================================
        # RESPONSABILIDAD MEZCLADA: Estado de la aplicación + configuración UI
        # =====================================================================
        self.history = []
        self.current_input = ""
        self.result = 0
        self.operator = None
        self.first_number = None
        self.waiting_for_second = False
        self.memory = 0
        self.dark_mode = False
        self.stats = {"sum": 0, "sub": 0, "mul": 0, "div": 0, "sci": 0}

        # =====================================================================
        # RESPONSABILIDAD MEZCLADA: Creación de ventana principal
        # =====================================================================
        self.window = tk.Tk()
        self.window.title("Calculadora")
        self.window.geometry("420x720")
        self.window.resizable(False, False)
        self.window.configure(bg="#1a1a2e")

        # =====================================================================
        # RESPONSABILIDAD MEZCLADA: Definición de colores y estilos (TEMA)
        # =====================================================================
        self.colors = {
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
            "fg_display": "#ffffff",
            "fg_button": "#ffffff",
            "fg_history": "#a0a0a0",
            "fg_clear": "#2d3436",
            "border": "#233554",
            "shadow": "#0d1117",
        }

        # =====================================================================
        # RESPONSABILIDAD MEZCLADA: Construcción completa de la interfaz
        # =====================================================================
        self._build_entire_interface()

    # =========================================================================
    #  RESPONSABILIDAD 1: CONSTRUCCIÓN DE LA INTERFAZ GRÁFICA
    #  (Debería estar en una clase separada de UI/Vista)
    # =========================================================================

    def _build_entire_interface(self):
        """Construye TODA la interfaz en un solo método gigante."""

        # --- Barra superior con título y botón de tema ---
        top_bar = tk.Frame(self.window, bg=self.colors["bg_main"], height=45)
        top_bar.pack(fill="x", padx=10, pady=(10, 0))
        top_bar.pack_propagate(False)

        title_label = tk.Label(
            top_bar,
            text="⚡ Calculadora Pro",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["bg_main"],
            fg="#e94560",
        )
        title_label.pack(side="left", padx=5)

        self.theme_btn = tk.Button(
            top_bar,
            text="🌙",
            font=("Segoe UI", 14),
            bg=self.colors["bg_main"],
            fg="#ffffff",
            bd=0,
            activebackground=self.colors["bg_main"],
            cursor="hand2",
            command=self.toggle_theme,
        )
        self.theme_btn.pack(side="right", padx=5)

        # --- Display / Pantalla ---
        display_frame = tk.Frame(
            self.window,
            bg=self.colors["bg_display"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )
        display_frame.pack(fill="x", padx=15, pady=(10, 5))

        self.history_label = tk.Label(
            display_frame,
            text="",
            font=("Segoe UI", 11),
            bg=self.colors["bg_display"],
            fg=self.colors["fg_history"],
            anchor="e",
        )
        self.history_label.pack(fill="x", padx=15, pady=(10, 0))

        self.display_var = tk.StringVar(value="0")
        self.display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Segoe UI Semibold", 36),
            bg=self.colors["bg_display"],
            fg=self.colors["fg_display"],
            anchor="e",
        )
        self.display_label.pack(fill="x", padx=15, pady=(0, 15))

        # --- Botones de memoria y acciones rápidas ---
        mem_frame = tk.Frame(self.window, bg=self.colors["bg_main"])
        mem_frame.pack(fill="x", padx=15, pady=2)

        memory_buttons = [
            ("MC", self.memory_clear),
            ("MR", self.memory_recall),
            ("M+", self.memory_add),
            ("M-", self.memory_subtract),
            ("📋 Hist", self.show_history_window),
            ("💾 Guardar", self.save_history_to_file),
        ]

        for text, cmd in memory_buttons:
            b = tk.Button(
                mem_frame,
                text=text,
                font=("Segoe UI", 9),
                bg="#233554",
                fg="#a0cfe4",
                bd=0,
                padx=6,
                pady=4,
                activebackground="#2c4a6e",
                activeforeground="#ffffff",
                cursor="hand2",
                command=cmd,
            )
            b.pack(side="left", expand=True, fill="x", padx=2)
            b.bind("<Enter>", lambda e, btn=b: btn.config(bg="#2c4a6e"))
            b.bind("<Leave>", lambda e, btn=b: btn.config(bg="#233554"))

        # --- Botones científicos ---
        sci_frame = tk.Frame(self.window, bg=self.colors["bg_main"])
        sci_frame.pack(fill="x", padx=15, pady=2)

        scientific_buttons = [
            ("√", self.sqrt_operation),
            ("x²", self.square_operation),
            ("%", self.percentage_operation),
            ("±", self.toggle_sign),
            ("π", self.insert_pi),
        ]

        for text, cmd in scientific_buttons:
            b = tk.Button(
                sci_frame,
                text=text,
                font=("Segoe UI", 12, "bold"),
                bg=self.colors["bg_scientific"],
                fg="#ffffff",
                bd=0,
                width=5,
                height=1,
                activebackground=self.colors["bg_scientific_hover"],
                activeforeground="#ffffff",
                cursor="hand2",
                command=cmd,
            )
            b.pack(side="left", expand=True, fill="x", padx=2, pady=2)
            b.bind(
                "<Enter>",
                lambda e, btn=b: btn.config(bg=self.colors["bg_scientific_hover"]),
            )
            b.bind(
                "<Leave>",
                lambda e, btn=b: btn.config(bg=self.colors["bg_scientific"]),
            )

        # --- Teclado numérico y operadores ---
        buttons_frame = tk.Frame(self.window, bg=self.colors["bg_main"])
        buttons_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        button_layout = [
            ("C", 0, 0, self.colors["bg_clear"], self.colors["fg_clear"], self.clear_all),
            ("⌫", 0, 1, self.colors["bg_clear"], self.colors["fg_clear"], self.backspace),
            ("(", 0, 2, "#233554", "#a0cfe4", lambda: self.append_to_input("(")),
            ("÷", 0, 3, self.colors["bg_operator"], "#fff", lambda: self.set_operator("/")),
            ("7", 1, 0, self.colors["bg_button"], "#fff", lambda: self.append_to_input("7")),
            ("8", 1, 1, self.colors["bg_button"], "#fff", lambda: self.append_to_input("8")),
            ("9", 1, 2, self.colors["bg_button"], "#fff", lambda: self.append_to_input("9")),
            ("×", 1, 3, self.colors["bg_operator"], "#fff", lambda: self.set_operator("*")),
            ("4", 2, 0, self.colors["bg_button"], "#fff", lambda: self.append_to_input("4")),
            ("5", 2, 1, self.colors["bg_button"], "#fff", lambda: self.append_to_input("5")),
            ("6", 2, 2, self.colors["bg_button"], "#fff", lambda: self.append_to_input("6")),
            ("−", 2, 3, self.colors["bg_operator"], "#fff", lambda: self.set_operator("-")),
            ("1", 3, 0, self.colors["bg_button"], "#fff", lambda: self.append_to_input("1")),
            ("2", 3, 1, self.colors["bg_button"], "#fff", lambda: self.append_to_input("2")),
            ("3", 3, 2, self.colors["bg_button"], "#fff", lambda: self.append_to_input("3")),
            ("+", 3, 3, self.colors["bg_operator"], "#fff", lambda: self.set_operator("+")),
            ("0", 4, 0, self.colors["bg_button"], "#fff", lambda: self.append_to_input("0")),
            ("00", 4, 1, self.colors["bg_button"], "#fff", lambda: self.append_to_input("00")),
            (".", 4, 2, self.colors["bg_button"], "#fff", lambda: self.append_to_input(".")),
            ("=", 4, 3, self.colors["bg_equal"], "#fff", self.calculate_result),
        ]

        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.columnconfigure(j, weight=1)

        for text, row, col, bg, fg, cmd in button_layout:
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=("Segoe UI", 18, "bold"),
                bg=bg,
                fg=fg,
                bd=0,
                activebackground=bg,
                activeforeground=fg,
                cursor="hand2",
                command=cmd,
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

            hover_color = self._get_hover_color(bg)
            btn.bind("<Enter>", lambda e, b=btn, hc=hover_color: b.config(bg=hc))
            btn.bind("<Leave>", lambda e, b=btn, oc=bg: b.config(bg=oc))

        # --- Barra inferior de estadísticas ---
        self.stats_label = tk.Label(
            self.window,
            text="Operaciones realizadas: 0",
            font=("Segoe UI", 9),
            bg=self.colors["bg_main"],
            fg="#636e72",
        )
        self.stats_label.pack(side="bottom", pady=(0, 8))

        # Enlazar teclado físico
        self.window.bind("<Key>", self.handle_keypress)

    # =========================================================================
    #  RESPONSABILIDAD 2: ESTILOS Y TEMAS VISUALES
    #  (Debería estar en una clase separada de Theme/StyleManager)
    # =========================================================================

    def _get_hover_color(self, base_color):
        """Calcula color hover — lógica de estilo mezclada con la clase."""
        hover_map = {
            self.colors["bg_button"]: self.colors["bg_button_hover"],
            self.colors["bg_operator"]: self.colors["bg_operator_hover"],
            self.colors["bg_equal"]: self.colors["bg_equal_hover"],
            self.colors["bg_clear"]: self.colors["bg_clear_hover"],
            self.colors["bg_scientific"]: self.colors["bg_scientific_hover"],
        }
        return hover_map.get(base_color, base_color)

    def toggle_theme(self):
        """Cambia entre tema oscuro y claro — responsabilidad de tema en la God Class."""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.window.configure(bg="#f5f6fa")
            self.theme_btn.config(text="☀️", bg="#f5f6fa")
            self.stats_label.config(bg="#f5f6fa", fg="#636e72")
        else:
            self.window.configure(bg="#1a1a2e")
            self.theme_btn.config(text="🌙", bg="#1a1a2e")
            self.stats_label.config(bg="#1a1a2e", fg="#636e72")

    # =========================================================================
    #  RESPONSABILIDAD 3: VALIDACIÓN DE ENTRADA
    #  (Debería estar en una clase separada de InputValidator)
    # =========================================================================

    def _validate_number(self, value):
        """Valida que un string sea un número válido."""
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def _validate_not_empty(self):
        """Valida que haya algo en el display."""
        current = self.display_var.get()
        if current == "" or current == "Error":
            messagebox.showwarning(
                "Entrada inválida",
                "Por favor ingrese un número válido.",
            )
            return False
        return True

    # =========================================================================
    #  RESPONSABILIDAD 4: LÓGICA DE OPERACIONES MATEMÁTICAS
    #  (Debería estar en una clase separada de MathEngine)
    # =========================================================================

    def append_to_input(self, char):
        """Agrega un carácter al input actual."""
        if self.waiting_for_second:
            self.current_input = ""
            self.waiting_for_second = False

        if char == "." and "." in self.current_input:
            return

        self.current_input += char
        self.display_var.set(self.current_input)

    def set_operator(self, op):
        """Establece el operador y guarda el primer número."""
        if self.current_input == "" and self.first_number is None:
            return

        if self.current_input != "":
            if self.first_number is not None and self.operator is not None:
                self.calculate_result()

            num = self._validate_number(self.current_input)
            if num is None:
                self.display_var.set("Error")
                return
            self.first_number = num

        self.operator = op
        op_symbol = {"+" : "+", "-": "−", "*": "×", "/": "÷"}.get(op, op)
        self.history_label.config(
            text=f"{self._format_number(self.first_number)} {op_symbol}"
        )
        self.current_input = ""
        self.waiting_for_second = False

    def calculate_result(self):
        """Realiza el cálculo — lógica matemática directamente en la God Class."""
        if self.operator is None or self.first_number is None:
            return

        second = self._validate_number(self.current_input)
        if second is None:
            self.display_var.set("Error")
            return

        result = None
        op_symbol = ""

        if self.operator == "+":
            result = self.first_number + second
            op_symbol = "+"
            self.stats["sum"] += 1
        elif self.operator == "-":
            result = self.first_number - second
            op_symbol = "−"
            self.stats["sub"] += 1
        elif self.operator == "*":
            result = self.first_number * second
            op_symbol = "×"
            self.stats["mul"] += 1
        elif self.operator == "/":
            if second == 0:
                self.display_var.set("Error")
                self.history_label.config(text="Error: División por cero")
                messagebox.showerror("Error", "No se puede dividir entre cero.")
                self._log_error("División por cero")
                self.current_input = ""
                self.operator = None
                self.first_number = None
                return
            result = self.first_number / second
            op_symbol = "÷"
            self.stats["div"] += 1

        # Formatear y mostrar resultado
        formatted = self._format_number(result)
        self.display_var.set(formatted)
        self.history_label.config(
            text=f"{self._format_number(self.first_number)} {op_symbol} {self._format_number(second)} ="
        )

        # Guardar en historial (mezcla de responsabilidades)
        timestamp = datetime.now().strftime("%H:%M:%S")
        record = {
            "expression": f"{self.first_number} {op_symbol} {second}",
            "result": result,
            "timestamp": timestamp,
        }
        self.history.append(record)

        # Actualizar estadísticas (otra responsabilidad más)
        total = sum(self.stats.values())
        self.stats_label.config(text=f"Operaciones realizadas: {total}")

        # Preparar para siguiente operación
        self.first_number = result
        self.current_input = formatted
        self.operator = None
        self.waiting_for_second = True

    # =========================================================================
    #  RESPONSABILIDAD 5: OPERACIONES CIENTÍFICAS
    #  (Debería estar en una clase separada de ScientificOperations)
    # =========================================================================

    def sqrt_operation(self):
        """Raíz cuadrada — operación científica en la God Class."""
        if not self._validate_not_empty():
            return
        num = self._validate_number(self.display_var.get())
        if num is None or num < 0:
            self.display_var.set("Error")
            messagebox.showerror("Error", "No se puede calcular raíz de un número negativo.")
            return
        result = math.sqrt(num)
        self.display_var.set(self._format_number(result))
        self.history_label.config(text=f"√({self._format_number(num)})")
        self.history.append({
            "expression": f"√({num})", "result": result,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        })
        self.current_input = self._format_number(result)
        self.stats["sci"] += 1
        self.stats_label.config(text=f"Operaciones realizadas: {sum(self.stats.values())}")

    def square_operation(self):
        """Elevar al cuadrado — más operaciones científicas aquí."""
        if not self._validate_not_empty():
            return
        num = self._validate_number(self.display_var.get())
        if num is None:
            self.display_var.set("Error")
            return
        result = num ** 2
        self.display_var.set(self._format_number(result))
        self.history_label.config(text=f"({self._format_number(num)})²")
        self.history.append({
            "expression": f"({num})²", "result": result,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        })
        self.current_input = self._format_number(result)
        self.stats["sci"] += 1
        self.stats_label.config(text=f"Operaciones realizadas: {sum(self.stats.values())}")

    def percentage_operation(self):
        """Porcentaje."""
        if not self._validate_not_empty():
            return
        num = self._validate_number(self.display_var.get())
        if num is None:
            self.display_var.set("Error")
            return
        result = num / 100
        self.display_var.set(self._format_number(result))
        self.history_label.config(text=f"{self._format_number(num)}%")
        self.current_input = self._format_number(result)

    def toggle_sign(self):
        """Cambiar signo +/-."""
        if not self._validate_not_empty():
            return
        num = self._validate_number(self.display_var.get())
        if num is None:
            return
        result = -num
        self.display_var.set(self._format_number(result))
        self.current_input = self._format_number(result)

    def insert_pi(self):
        """Insertar valor de PI."""
        self.current_input = str(math.pi)
        self.display_var.set(self._format_number(math.pi))

    # =========================================================================
    #  RESPONSABILIDAD 6: GESTIÓN DE MEMORIA
    #  (Debería estar en una clase separada de MemoryManager)
    # =========================================================================

    def memory_clear(self):
        self.memory = 0
        messagebox.showinfo("Memoria", "Memoria limpiada.")

    def memory_recall(self):
        self.current_input = self._format_number(self.memory)
        self.display_var.set(self.current_input)

    def memory_add(self):
        num = self._validate_number(self.display_var.get())
        if num is not None:
            self.memory += num

    def memory_subtract(self):
        num = self._validate_number(self.display_var.get())
        if num is not None:
            self.memory -= num

    # =========================================================================
    #  RESPONSABILIDAD 7: GESTIÓN DEL HISTORIAL
    #  (Debería estar en una clase separada de HistoryManager)
    # =========================================================================

    def show_history_window(self):
        """Abre una ventana para mostrar el historial — UI + datos mezclados."""
        hist_window = tk.Toplevel(self.window)
        hist_window.title("Historial de Operaciones")
        hist_window.geometry("380x450")
        hist_window.configure(bg=self.colors["bg_main"])
        hist_window.resizable(False, False)

        header = tk.Label(
            hist_window,
            text="📋 Historial de Operaciones",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["bg_main"],
            fg="#e94560",
        )
        header.pack(pady=(15, 10))

        if not self.history:
            tk.Label(
                hist_window,
                text="No hay operaciones registradas.",
                font=("Segoe UI", 11),
                bg=self.colors["bg_main"],
                fg="#a0a0a0",
            ).pack(pady=20)
        else:
            canvas = tk.Canvas(hist_window, bg=self.colors["bg_main"], highlightthickness=0)
            scrollbar = tk.Scrollbar(hist_window, orient="vertical", command=canvas.yview)
            scroll_frame = tk.Frame(canvas, bg=self.colors["bg_main"])

            scroll_frame.bind(
                "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            for i, record in enumerate(reversed(self.history), 1):
                item_frame = tk.Frame(
                    scroll_frame,
                    bg=self.colors["bg_display"],
                    highlightbackground=self.colors["border"],
                    highlightthickness=1,
                )
                item_frame.pack(fill="x", padx=15, pady=3)

                tk.Label(
                    item_frame,
                    text=f"  {record['expression']} = {self._format_number(record['result'])}",
                    font=("Segoe UI", 11),
                    bg=self.colors["bg_display"],
                    fg="#ffffff",
                    anchor="w",
                ).pack(fill="x", padx=5, pady=(5, 0))

                tk.Label(
                    item_frame,
                    text=f"  🕐 {record['timestamp']}",
                    font=("Segoe UI", 8),
                    bg=self.colors["bg_display"],
                    fg="#636e72",
                    anchor="w",
                ).pack(fill="x", padx=5, pady=(0, 5))

            canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
            scrollbar.pack(side="right", fill="y")

        # Botones de acción en historial (más mezcla de responsabilidades)
        btn_frame = tk.Frame(hist_window, bg=self.colors["bg_main"])
        btn_frame.pack(fill="x", padx=15, pady=10)

        tk.Button(
            btn_frame, text="🗑️ Limpiar historial", font=("Segoe UI", 10),
            bg="#e94560", fg="#fff", bd=0, padx=10, pady=5, cursor="hand2",
            command=lambda: self._clear_history_and_close(hist_window),
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame, text="📊 Estadísticas", font=("Segoe UI", 10),
            bg="#6c5ce7", fg="#fff", bd=0, padx=10, pady=5, cursor="hand2",
            command=self.show_statistics,
        ).pack(side="right", padx=5)

    def _clear_history_and_close(self, window):
        """Limpia historial y cierra ventana."""
        self.history.clear()
        self.stats = {"sum": 0, "sub": 0, "mul": 0, "div": 0, "sci": 0}
        self.stats_label.config(text="Operaciones realizadas: 0")
        window.destroy()
        messagebox.showinfo("Historial", "Historial limpiado correctamente.")

    # =========================================================================
    #  RESPONSABILIDAD 8: PERSISTENCIA / ARCHIVOS
    #  (Debería estar en una clase separada de FileManager/Repository)
    # =========================================================================

    def save_history_to_file(self):
        """Guarda historial a archivo — I/O directamente en la God Class."""
        if not self.history:
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
            if filepath.endswith(".json"):
                data = {
                    "calculator_history": self.history,
                    "statistics": self.stats,
                    "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "total_operations": sum(self.stats.values()),
                }
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            else:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("=== HISTORIAL DE LA CALCULADORA ===\n")
                    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 40 + "\n\n")
                    for record in self.history:
                        f.write(
                            f"[{record['timestamp']}] "
                            f"{record['expression']} = {record['result']}\n"
                        )
                    f.write(f"\nTotal de operaciones: {sum(self.stats.values())}\n")

            messagebox.showinfo("Guardado", f"Historial guardado en:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")
            self._log_error(f"Error al guardar archivo: {e}")

    def _log_error(self, error_msg):
        """Registra errores en un archivo de log — más I/O en la God Class."""
        try:
            log_dir = os.path.dirname(os.path.abspath(__file__))
            log_path = os.path.join(log_dir, "calculator_errors.log")
            with open(log_path, "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {error_msg}\n")
        except Exception:
            pass

    # =========================================================================
    #  RESPONSABILIDAD 9: ESTADÍSTICAS Y REPORTES
    #  (Debería estar en una clase separada de StatisticsReporter)
    # =========================================================================

    def show_statistics(self):
        """Muestra estadísticas — generación de reportes en la God Class."""
        total = sum(self.stats.values())
        msg = (
            f"📊 Estadísticas de Uso\n"
            f"{'─' * 30}\n"
            f"  Sumas:                {self.stats['sum']}\n"
            f"  Restas:               {self.stats['sub']}\n"
            f"  Multiplicaciones:  {self.stats['mul']}\n"
            f"  Divisiones:           {self.stats['div']}\n"
            f"  Científicas:          {self.stats['sci']}\n"
            f"{'─' * 30}\n"
            f"  TOTAL:                {total}\n"
        )

        if self.history:
            results = [r["result"] for r in self.history]
            msg += (
                f"\n📈 Análisis de Resultados\n"
                f"{'─' * 30}\n"
                f"  Máximo:  {max(results)}\n"
                f"  Mínimo:   {min(results)}\n"
                f"  Promedio: {sum(results) / len(results):.4f}\n"
            )

        messagebox.showinfo("Estadísticas", msg)

    # =========================================================================
    #  RESPONSABILIDAD 10: UTILIDADES Y FORMATEO
    #  (Debería estar en una clase separada de Formatter/Utils)
    # =========================================================================

    def _format_number(self, number):
        """Formatea un número para mostrar."""
        if number is None:
            return "Error"
        if isinstance(number, float) and number == int(number):
            return str(int(number))
        if isinstance(number, float):
            return f"{number:.8g}"
        return str(number)

    def clear_all(self):
        """Limpia toda la calculadora."""
        self.current_input = ""
        self.first_number = None
        self.operator = None
        self.waiting_for_second = False
        self.display_var.set("0")
        self.history_label.config(text="")

    def backspace(self):
        """Borra el último carácter."""
        self.current_input = self.current_input[:-1]
        self.display_var.set(self.current_input if self.current_input else "0")

    # =========================================================================
    #  RESPONSABILIDAD 11: MANEJO DE EVENTOS DEL TECLADO
    #  (Debería estar en una clase separada de InputHandler/EventController)
    # =========================================================================

    def handle_keypress(self, event):
        """Maneja las teclas del teclado — event handling en la God Class."""
        key = event.char
        keysym = event.keysym

        if key in "0123456789":
            self.append_to_input(key)
        elif key == ".":
            self.append_to_input(".")
        elif key == "+":
            self.set_operator("+")
        elif key == "-":
            self.set_operator("-")
        elif key == "*":
            self.set_operator("*")
        elif key == "/":
            self.set_operator("/")
        elif keysym == "Return" or key == "=":
            self.calculate_result()
        elif keysym == "BackSpace":
            self.backspace()
        elif keysym == "Escape":
            self.clear_all()
        elif keysym == "Delete":
            self.clear_all()

    # =========================================================================
    #  MÉTODO PRINCIPAL: EJECUTAR LA APLICACIÓN
    # =========================================================================

    def run(self):
        """Inicia el loop principal de la aplicación."""
        self.window.mainloop()


# =============================================================================
# PUNTO DE ENTRADA — Todo se ejecuta desde la God Class
# =============================================================================

if __name__ == "__main__":
    app = Calculator()
    app.run()
