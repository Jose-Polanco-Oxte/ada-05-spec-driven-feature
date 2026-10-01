"""
Search service providing text normalization, query validation, and customer filtering.
"""

from __future__ import annotations
import unicodedata
from typing import List, Optional

from src.models import Customer
from src.repository import CustomerRepository
from src.exceptions import (
    EmptyQueryError,
    QueryTooShortError,
    InvalidFieldError,
    InvalidStatusFilterError,
)


def normalize_text(text: Optional[str]) -> str:
    """
    Normaliza una cadena de texto eliminando marcas diacríticas (acentos)
    y convirtiéndola a minúsculas para comparaciones insensibles.
    """
    if not text:
        return ""
    # Descomposición canónica NFKD: separa letras de sus acentos
    nfkd_form = unicodedata.normalize("NFKD", text)
    # Filtra caracteres de categoría 'Mn' (Nonspacing Mark / tildes y diacríticos)
    without_diacritics = "".join(
        char for char in nfkd_form if unicodedata.category(char) != "Mn"
    )
    return without_diacritics.lower().strip()


class CustomerSearchService:
    """
    Servicio encargado de validar consultas y realizar la búsqueda de clientes.
    """

    ALLOWED_FIELDS = {"all", "name", "email", "phone"}
    ALLOWED_STATUSES = {"all", "active", "inactive"}

    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def validate_query(self, query: Optional[str]) -> str:
        """
        Valida que el término de búsqueda cumpla las reglas V-01 y V-02.
        Retorna la consulta limpia si es válida.
        """
        if query is None or not query.strip():
            raise EmptyQueryError("El término de búsqueda no puede estar vacío.")

        cleaned = query.strip()
        if len(cleaned) < 2:
            raise QueryTooShortError("El término de búsqueda debe tener al menos 2 caracteres.")

        return cleaned

    def validate_criteria(self, field: str, status_filter: str) -> None:
        """
        Valida que el campo y filtro de estado pertenezcan a los permitidos.
        """
        if field not in self.ALLOWED_FIELDS:
            raise InvalidFieldError(
                f"Campo '{field}' no válido. Opciones permitidas: {', '.join(sorted(self.ALLOWED_FIELDS))}"
            )
        if status_filter not in self.ALLOWED_STATUSES:
            raise InvalidStatusFilterError(
                f"Filtro de estado '{status_filter}' no válido. Opciones permitidas: {', '.join(sorted(self.ALLOWED_STATUSES))}"
            )

    def search(
        self,
        query: str,
        field: str = "all",
        status_filter: str = "all"
    ) -> List[Customer]:
        """
        Ejecuta la búsqueda de clientes según los criterios provistos.

        :param query: Término de búsqueda a buscar parcialmente.
        :param field: Campo a evaluar ('all', 'name', 'email').
        :param status_filter: Filtro de estado ('all', 'active', 'inactive').
        :return: Lista de clientes coincidentes ordenados alfabéticamente por nombre.
        """
        cleaned_query = self.validate_query(query)
        self.validate_criteria(field, status_filter)

        norm_query = normalize_text(cleaned_query)
        all_customers = self.repository.get_all()

        results: List[Customer] = []
        for customer in all_customers:
            # 1. Filtro por estado
            if status_filter == "active" and not customer.is_active:
                continue
            if status_filter == "inactive" and customer.is_active:
                continue

            # 2. Evaluación de coincidencia según campo
            match = False
            norm_name = normalize_text(customer.name)
            norm_email = normalize_text(customer.email)
            norm_phone = normalize_text(customer.phone)

            if field == "name":
                match = norm_query in norm_name
            elif field == "email":
                match = norm_query in norm_email
            elif field == "phone":
                match = norm_query in norm_phone
            elif field == "all":
                match = (norm_query in norm_name) or (norm_query in norm_email) or (norm_query in norm_phone)

            if match:
                results.append(customer)

        # 3. Ordenamiento alfabético ascendente por nombre
        results.sort(key=lambda c: normalize_text(c.name))
        return results
