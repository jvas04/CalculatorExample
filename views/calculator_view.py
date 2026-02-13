# =============================================================================
# SRP: CalculatorView - ÚNICA responsabilidad: construir y actualizar la UI
# Alta Cohesión: todos los métodos crean o modifican widgets de la interfaz
# =============================================================================

import tkinter as tk


class CalculatorView:
    """
    Construye y actualiza la interfaz gráfica de la calculadora.

    Responsabilidad única: crear widgets y actualizar elementos visuales.
    Alta cohesión: todos los métodos construyen o modifican componentes de UI.

    Razón para cambiar: solo si cambia el layout o los componentes de la interfaz.

    NOTA: Esta clase NO contiene lógica de negocio. Los callbacks de los
    botones son inyectados por el Controller, manteniendo la separación.
    """

    def __init__(self, window: tk.Tk, colors: dict):
        self.window = window
        self.colors = colors

        # Variables de display
        self.display_var = tk.StringVar(value="0")
        self.history_label = None
        self.display_label = None
        self.stats_label = None
        self.theme_btn = None

        # Almacenar botones para poder actualizar temas
        self._buttons = []
        self._mem_buttons = []
        self._sci_buttons = []

    # -------------------------------------------------------------------------
    #  Configuración de la ventana principal
    # -------------------------------------------------------------------------

    def setup_window(self) -> None:
        """Configura las propiedades de la ventana principal."""
        self.window.title("Calculadora")
        self.window.geometry("420x720")
        self.window.resizable(False, False)
        self.window.configure(bg=self.colors["bg_main"])

    # -------------------------------------------------------------------------
    #  Construcción de secciones de la interfaz
    # -------------------------------------------------------------------------

    def build_top_bar(self, on_toggle_theme) -> None:
        """Construye la barra superior con título y botón de tema."""
        top_bar = tk.Frame(self.window, bg=self.colors["bg_main"], height=45)
        top_bar.pack(fill="x", padx=10, pady=(10, 0))
        top_bar.pack_propagate(False)

        tk.Label(
            top_bar,
            text="⚡ Calculadora Pro",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["bg_main"],
            fg=self.colors["fg_title"],
        ).pack(side="left", padx=5)

        self.theme_btn = tk.Button(
            top_bar,
            text="🌙",
            font=("Segoe UI", 14),
            bg=self.colors["bg_main"],
            fg="#ffffff",
            bd=0,
            activebackground=self.colors["bg_main"],
            cursor="hand2",
            command=on_toggle_theme,
        )
        self.theme_btn.pack(side="right", padx=5)

    def build_display(self) -> None:
        """Construye la pantalla/display de la calculadora."""
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

        self.display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Segoe UI Semibold", 36),
            bg=self.colors["bg_display"],
            fg=self.colors["fg_display"],
            anchor="e",
        )
        self.display_label.pack(fill="x", padx=15, pady=(0, 15))

    def build_memory_buttons(self, callbacks: list[tuple]) -> None:
        """
        Construye los botones de memoria y acciones rápidas.
        callbacks: lista de tuplas (texto, función_callback).
        """
        mem_frame = tk.Frame(self.window, bg=self.colors["bg_main"])
        mem_frame.pack(fill="x", padx=15, pady=2)

        for text, cmd in callbacks:
            b = tk.Button(
                mem_frame,
                text=text,
                font=("Segoe UI", 9),
                bg=self.colors["bg_memory"],
                fg=self.colors["fg_memory"],
                bd=0,
                padx=6,
                pady=4,
                activebackground=self.colors["bg_memory_hover"],
                activeforeground="#ffffff",
                cursor="hand2",
                command=cmd,
            )
            b.pack(side="left", expand=True, fill="x", padx=2)
            b.bind(
                "<Enter>",
                lambda e, btn=b: btn.config(bg=self.colors["bg_memory_hover"]),
            )
            b.bind(
                "<Leave>",
                lambda e, btn=b: btn.config(bg=self.colors["bg_memory"]),
            )
            self._mem_buttons.append(b)

    def build_scientific_buttons(self, callbacks: list[tuple]) -> None:
        """
        Construye los botones científicos.
        callbacks: lista de tuplas (texto, función_callback).
        """
        sci_frame = tk.Frame(self.window, bg=self.colors["bg_main"])
        sci_frame.pack(fill="x", padx=15, pady=2)

        for text, cmd in callbacks:
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
            self._sci_buttons.append(b)

    def build_keypad(self, button_layout: list[tuple], get_hover_color) -> None:
        """
        Construye el teclado numérico y de operadores.
        button_layout: lista de tuplas (texto, fila, col, bg, fg, callback).
        get_hover_color: función que dado un color base retorna el hover.
        """
        buttons_frame = tk.Frame(self.window, bg=self.colors["bg_main"])
        buttons_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))

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

            hover_color = get_hover_color(bg)
            btn.bind("<Enter>", lambda e, b=btn, hc=hover_color: b.config(bg=hc))
            btn.bind("<Leave>", lambda e, b=btn, oc=bg: b.config(bg=oc))

            self._buttons.append((btn, bg, fg))

    def build_stats_bar(self) -> None:
        """Construye la barra inferior de estadísticas."""
        self.stats_label = tk.Label(
            self.window,
            text="Operaciones realizadas: 0",
            font=("Segoe UI", 9),
            bg=self.colors["bg_main"],
            fg=self.colors["fg_stats"],
        )
        self.stats_label.pack(side="bottom", pady=(0, 8))

    # -------------------------------------------------------------------------
    #  Métodos de actualización del display
    # -------------------------------------------------------------------------

    def update_display(self, value: str) -> None:
        """Actualiza el valor mostrado en el display principal."""
        self.display_var.set(value)

    def update_history_text(self, text: str) -> None:
        """Actualiza el texto de la expresión sobre el display."""
        self.history_label.config(text=text)

    def update_stats_text(self, text: str) -> None:
        """Actualiza el texto de la barra de estadísticas."""
        self.stats_label.config(text=text)

    def update_theme(self, colors: dict, icon: str) -> None:
        """Actualiza los colores de la ventana y el botón de tema."""
        self.colors = colors
        self.window.configure(bg=colors["bg_main"])
        self.theme_btn.config(text=icon, bg=colors["bg_main"])
        self.stats_label.config(bg=colors["bg_main"], fg=colors["fg_stats"])

    def get_display_value(self) -> str:
        """Retorna el valor actual del display."""
        return self.display_var.get()

    def bind_keyboard(self, handler) -> None:
        """Enlaza el handler de teclado a la ventana."""
        self.window.bind("<Key>", handler)
