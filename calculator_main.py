import tkinter as tk

from utils.theme_manager import ThemeManager
from views.calculator_view import CalculatorView
from controllers.calculator_controller import CalculatorController


def main():
    """Punto de entrada: crea la ventana, la vista, el controlador e inicia."""
    window = tk.Tk()

    theme = ThemeManager()
    colors = theme.get_colors()

    view = CalculatorView(window, colors)
    controller = CalculatorController(view)
    controller.initialize()

    window.mainloop()


if __name__ == "__main__":
    main()
