"""
Unit tests for CustomerSearchService search logic.
"""

import pytest
from src.models import Customer
from src.repository import CustomerRepository
from src.search_service import CustomerSearchService, normalize_text


@pytest.fixture
def sample_customers():
    return [
        Customer(id="C-1", name="Carlos García Pérez", email="carlos.garcia@uady.mx", is_active=True),
        Customer(id="C-2", name="José Ángel Morales", email="jose.morales@corp.com", is_active=False),
        Customer(id="C-3", name="María Gómez", email="maria@example.com", is_active=True),
        Customer(id="C-4", name="Roberto Gómez", email="alex.gomez@mail.com", is_active=True),
        Customer(id="C-5", name="Ana Sofía Ruiz", email="asofia@instituto.edu", is_active=False),
    ]


@pytest.fixture
def search_service(sample_customers):
    repo = CustomerRepository(data_source=sample_customers)
    return CustomerSearchService(repository=repo)


def test_normalize_text():
    assert normalize_text("José María") == "jose maria"
    assert normalize_text("ÁÉÍÓÚ ñ") == "aeiou n"
    assert normalize_text("   TEST   ") == "test"
    assert normalize_text("") == ""
    assert normalize_text(None) == ""


def test_search_by_name_partial_case_insensitive_and_accents(search_service):
    # FR-01, AC-01: 'garcia' finds 'Carlos García Pérez'
    results = search_service.search("garcia", field="name")
    assert len(results) == 1
    assert results[0].id == "C-1"

    # Searching with accent 'GÓMEZ' finds 'María Gómez' and 'Roberto Gómez'
    results_accent = search_service.search("GÓMEZ", field="name")
    assert len(results_accent) == 2
    assert [c.id for c in results_accent] == ["C-3", "C-4"]


def test_search_by_email_partial(search_service):
    # FR-02, AC-02: 'corp.com' finds 'jose.morales@corp.com'
    results = search_service.search("CORP.COM", field="email")
    assert len(results) == 1
    assert results[0].id == "C-2"

    # 'uady' finds 'carlos.garcia@uady.mx'
    results_uady = search_service.search("uady", field="email")
    assert len(results_uady) == 1
    assert results_uady[0].id == "C-1"


def test_search_global_all_fields(search_service):
    # FR-03, AC-03: 'alex' matches Roberto Gómez's email ('alex.gomez@mail.com')
    results = search_service.search("alex", field="all")
    assert len(results) == 1
    assert results[0].name == "Roberto Gómez"

    # 'gomez' matches María Gómez (name) and Roberto Gómez (name + email)
    results_gomez = search_service.search("gomez", field="all")
    assert len(results_gomez) == 2
    assert [c.name for c in results_gomez] == ["María Gómez", "Roberto Gómez"]


def test_search_status_filter(search_service):
    # FR-05, AC-05: Filter active only vs inactive only
    active_results = search_service.search("gomez", field="name", status_filter="active")
    assert len(active_results) == 2

    # Search for 'morales' (which is inactive)
    inactive_results = search_service.search("morales", field="name", status_filter="inactive")
    assert len(inactive_results) == 1
    assert inactive_results[0].id == "C-2"

    # When filtered active, it shouldn't show up
    empty_active = search_service.search("morales", field="name", status_filter="active")
    assert len(empty_active) == 0


def test_search_no_matches_returns_empty_list(search_service):
    # Scenario 6: Searching for non-existent text returns empty list
    results = search_service.search("ZzzzzNotFound", field="all")
    assert results == []


def test_search_results_alphabetical_order(search_service):
    results = search_service.search("com", field="email")
    # jose.morales@corp.com, maria@example.com, alex.gomez@mail.com
    names = [c.name for c in results]
    assert names == sorted(names, key=normalize_text)


def test_search_by_phone_partial():
    customers = [
        Customer(id="C-P1", name="Carlos García", email="carlos@example.com", phone="+52 999 123 4567"),
        Customer(id="C-P2", name="Ana Ruiz", email="ana@example.com", phone="+52 999 987 6543"),
    ]
    service = CustomerSearchService(repository=CustomerRepository(data_source=customers))
    results = service.search("123", field="phone")
    assert len(results) == 1
    assert results[0].id == "C-P1"

    results_all = service.search("987", field="all")
    assert len(results_all) == 1
    assert results_all[0].id == "C-P2"

