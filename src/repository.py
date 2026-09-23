"""
Repository layer for Customer data access.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import List, Optional, Union

from src.models import Customer
from src.exceptions import CustomerRepositoryError


class CustomerRepository:
    """
    Repositorio de datos para el acceso y carga de clientes desde archivo JSON o memoria.
    """

    def __init__(self, data_source: Optional[Union[str, Path, List[Customer]]] = None):
        self._customers: List[Customer] = []
        if isinstance(data_source, list):
            self._customers = list(data_source)
        else:
            if data_source is None:
                # Default path relative to workspace or repository
                default_path = Path("data") / "customers.json"
                self._load_from_file(default_path)
            else:
                self._load_from_file(Path(data_source))

    def _load_from_file(self, file_path: Path) -> None:
        if not file_path.exists():
            raise CustomerRepositoryError(f"No se encontró el archivo de datos: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            if not isinstance(raw_data, list):
                raise CustomerRepositoryError("El archivo JSON debe contener una lista de clientes.")
            self._customers = [Customer.from_dict(item) for item in raw_data]
        except json.JSONDecodeError as exc:
            raise CustomerRepositoryError(f"Error de formato JSON en {file_path}: {exc}") from exc
        except Exception as exc:
            if isinstance(exc, CustomerRepositoryError):
                raise
            raise CustomerRepositoryError(f"Error inesperado al cargar clientes: {exc}") from exc

    def get_all(self) -> List[Customer]:
        """Retorna una copia de la lista de todos los clientes disponibles."""
        return list(self._customers)

    def count(self) -> int:
        """Retorna el número total de clientes en el repositorio."""
        return len(self._customers)
