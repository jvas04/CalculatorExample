# =============================================================================
# SRP: HistoryView - ÚNICA responsabilidad: mostrar la ventana de historial
# Alta Cohesión: todos los métodos construyen o controlan la ventana de historial
# =============================================================================

import tkinter as tk


class HistoryView:
    """
    Construye y gestiona la ventana emergente del historial de operaciones.

    Responsabilidad única: mostrar el historial en una ventana separada.
    Alta cohesión: todos los métodos se relacionan con la ventana de historial.

    Razón para cambiar: solo si cambia la presentación del historial.
    """

    def __init__(self, parent: tk.Tk, colors: dict):
        self._parent = parent
        self._colors = colors

    def show(
        self,
        records: list[dict],
        format_number,
        on_clear: callable,
        on_statistics: callable,
    ) -> None:
        """Abre la ventana de historial con los registros proporcionados."""
        hist_window = tk.Toplevel(self._parent)
        hist_window.title("Historial de Operaciones")
        hist_window.geometry("380x450")
        hist_window.configure(bg=self._colors["bg_main"])
        hist_window.resizable(False, False)

        # Header
        tk.Label(
            hist_window,
            text="📋 Historial de Operaciones",
            font=("Segoe UI", 14, "bold"),
            bg=self._colors["bg_main"],
            fg="#e94560",
        ).pack(pady=(15, 10))

        # Contenido
        if not records:
            tk.Label(
                hist_window,
                text="No hay operaciones registradas.",
                font=("Segoe UI", 11),
                bg=self._colors["bg_main"],
                fg="#a0a0a0",
            ).pack(pady=20)
        else:
            self._build_records_list(hist_window, records, format_number)

        # Botones de acción
        self._build_action_buttons(hist_window, on_clear, on_statistics)

    def _build_records_list(
        self, parent_window: tk.Toplevel, records: list[dict], format_number
    ) -> None:
        """Construye la lista scrollable de registros del historial."""
        canvas = tk.Canvas(
            parent_window, bg=self._colors["bg_main"], highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            parent_window, orient="vertical", command=canvas.yview
        )
        scroll_frame = tk.Frame(canvas, bg=self._colors["bg_main"])

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for record in records:
            item_frame = tk.Frame(
                scroll_frame,
                bg=self._colors["bg_display"],
                highlightbackground=self._colors["border"],
                highlightthickness=1,
            )
            item_frame.pack(fill="x", padx=15, pady=3)

            tk.Label(
                item_frame,
                text=f"  {record['expression']} = {format_number(record['result'])}",
                font=("Segoe UI", 11),
                bg=self._colors["bg_display"],
                fg="#ffffff",
                anchor="w",
            ).pack(fill="x", padx=5, pady=(5, 0))

            tk.Label(
                item_frame,
                text=f"  🕐 {record['timestamp']}",
                font=("Segoe UI", 8),
                bg=self._colors["bg_display"],
                fg="#636e72",
                anchor="w",
            ).pack(fill="x", padx=5, pady=(0, 5))

        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
        scrollbar.pack(side="right", fill="y")

    def _build_action_buttons(
        self, parent_window: tk.Toplevel, on_clear: callable, on_statistics: callable
    ) -> None:
        """Construye los botones de acción de la ventana de historial."""
        btn_frame = tk.Frame(parent_window, bg=self._colors["bg_main"])
        btn_frame.pack(fill="x", padx=15, pady=10)

        tk.Button(
            btn_frame,
            text="🗑️ Limpiar historial",
            font=("Segoe UI", 10),
            bg="#e94560",
            fg="#fff",
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
            command=lambda: self._on_clear_and_close(parent_window, on_clear),
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="📊 Estadísticas",
            font=("Segoe UI", 10),
            bg="#6c5ce7",
            fg="#fff",
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
            command=on_statistics,
        ).pack(side="right", padx=5)

    def _on_clear_and_close(self, window: tk.Toplevel, on_clear: callable) -> None:
        """Ejecuta el callback de limpiar y cierra la ventana."""
        on_clear()
        window.destroy()
