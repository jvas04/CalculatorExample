# =============================================================================
# SRP: ErrorLogger - ÚNICA responsabilidad: registrar errores en archivo de log
# Alta Cohesión: todos los métodos se relacionan con el logging de errores
# =============================================================================

import os
from datetime import datetime


class ErrorLogger:
    """
    Registra errores de la aplicación en un archivo de log.

    Responsabilidad única: escribir mensajes de error en un archivo de log.
    Alta cohesión: todos los métodos se relacionan con el registro de errores.

    Razón para cambiar: solo si cambia el formato o destino del log.
    """

    def __init__(self, log_filename: str = "calculator_errors.log"):
        log_dir = os.path.dirname(os.path.abspath(__file__))
        self._log_path = os.path.join(log_dir, log_filename)

    def log(self, error_msg: str) -> None:
        """Registra un mensaje de error con timestamp en el archivo de log."""
        try:
            with open(self._log_path, "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {error_msg}\n")
        except Exception:
            pass

    def get_log_path(self) -> str:
        """Retorna la ruta del archivo de log."""
        return self._log_path
