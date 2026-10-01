"""
Unit tests for search query validation and exception handling.
"""

import pytest
from src.exceptions import (
    EmptyQueryError,
    QueryTooShortError,
    InvalidFieldError,
    InvalidStatusFilterError,
    CustomerRepositoryError,
)
from src.repository import CustomerRepository
from src.search_service import CustomerSearchService


@pytest.fixture
def dummy_service():
    repo = CustomerRepository(data_source=[])
    return CustomerSearchService(repository=repo)


def test_empty_query_error(dummy_service):
    # FR-04, AC-04
    with pytest.raises(EmptyQueryError, match="El término de búsqueda no puede estar vacío."):
        dummy_service.search("")

    with pytest.raises(EmptyQueryError, match="El término de búsqueda no puede estar vacío."):
        dummy_service.search("     ")

    with pytest.raises(EmptyQueryError, match="El término de búsqueda no puede estar vacío."):
        dummy_service.search(None)  # type: ignore


def test_query_too_short_error(dummy_service):
    # FR-04, AC-04
    with pytest.raises(QueryTooShortError, match="El término de búsqueda debe tener al menos 2 caracteres."):
        dummy_service.search("a")

    with pytest.raises(QueryTooShortError, match="El término de búsqueda debe tener al menos 2 caracteres."):
        dummy_service.search("  x  ")


def test_invalid_field_error(dummy_service):
    with pytest.raises(InvalidFieldError, match="Campo 'address' no válido."):
        dummy_service.search("test", field="address")


def test_invalid_status_filter_error(dummy_service):
    with pytest.raises(InvalidStatusFilterError, match="Filtro de estado 'pending' no válido."):
        dummy_service.search("test", status_filter="pending")


def test_repository_file_not_found():
    with pytest.raises(CustomerRepositoryError, match="No se encontró el archivo de datos"):
        CustomerRepository(data_source="non_existent_file.json")


def test_repository_invalid_json(tmp_path):
    bad_json_file = tmp_path / "corrupt.json"
    bad_json_file.write_text("{ not valid json }", encoding="utf-8")
    with pytest.raises(CustomerRepositoryError, match="Error de formato JSON"):
        CustomerRepository(data_source=bad_json_file)


def test_repository_non_list_json(tmp_path):
    dict_json_file = tmp_path / "not_a_list.json"
    dict_json_file.write_text('{"name": "single"}', encoding="utf-8")
    with pytest.raises(CustomerRepositoryError, match="El archivo JSON debe contener una lista"):
        CustomerRepository(data_source=dict_json_file)
