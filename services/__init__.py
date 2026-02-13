# Paquete services: Servicios auxiliares (I/O, logging)
# Cada módulo gestiona un servicio externo con responsabilidad única (SRP)

from services.file_manager import FileManager
from services.error_logger import ErrorLogger

__all__ = [
    "FileManager",
    "ErrorLogger",
]
