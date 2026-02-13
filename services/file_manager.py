# =============================================================================
# SRP: FileManager - ÚNICA responsabilidad: persistir datos en archivos
# Alta Cohesión: todos los métodos se relacionan con lectura/escritura de archivos
# =============================================================================

import json
from datetime import datetime


class FileManager:
    """
    Gestiona la persistencia de datos en archivos (guardar/cargar).

    Responsabilidad única: leer y escribir datos en el sistema de archivos.
    Alta cohesión: todos los métodos realizan operaciones de I/O con archivos.

    Razón para cambiar: solo si cambia el formato o destino de persistencia.
    """

    @staticmethod
    def save_as_json(filepath: str, history: list[dict], stats: dict) -> None:
        """Guarda historial y estadísticas en formato JSON."""
        data = {
            "calculator_history": history,
            "statistics": stats,
            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_operations": sum(stats.values()),
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def save_as_text(filepath: str, history: list[dict], stats: dict) -> None:
        """Guarda historial en formato de texto plano."""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=== HISTORIAL DE LA CALCULADORA ===\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 40 + "\n\n")
            for record in history:
                f.write(
                    f"[{record['timestamp']}] "
                    f"{record['expression']} = {record['result']}\n"
                )
            f.write(f"\nTotal de operaciones: {sum(stats.values())}\n")

    def save(self, filepath: str, history: list[dict], stats: dict) -> None:
        """
        Guarda el historial en el formato adecuado según la extensión del archivo.
        Lanza excepción si hay error de I/O (el llamador la maneja).
        """
        if filepath.endswith(".json"):
            self.save_as_json(filepath, history, stats)
        else:
            self.save_as_text(filepath, history, stats)
