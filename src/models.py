"""
Domain models for Customer Search.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Customer:
    """
    Entidad inmutable que representa a un cliente en el sistema.
    """
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    is_active: bool = True
    created_at: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("El 'id' del cliente no puede estar vacío.")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("El 'name' del cliente no puede estar vacío.")
        if not isinstance(self.email, str) or not self.email.strip():
            raise ValueError("El 'email' del cliente no puede estar vacío.")
        if not isinstance(self.is_active, bool):
            raise TypeError("El campo 'is_active' debe ser un booleano.")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Customer:
        """Crea una instancia de Customer a partir de un diccionario."""
        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            email=str(data.get("email", "")),
            phone=data.get("phone"),
            is_active=bool(data.get("is_active", True)),
            created_at=str(data.get("created_at", ""))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad Customer a un diccionario serializable."""
        return asdict(self)
