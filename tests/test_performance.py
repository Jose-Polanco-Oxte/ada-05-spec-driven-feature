"""
Performance and latency tests for CustomerSearchService (NFR-01).
"""

import time
import pytest
from src.models import Customer
from src.repository import CustomerRepository
from src.search_service import CustomerSearchService


def test_search_latency_under_50ms_for_1000_customers():
    """
    NFR-01: La búsqueda en memoria o JSON para 1,000 registros
    debe completarse estrictamente en menos de 50 milisegundos.
    """
    # Generar 1,000 clientes sintéticos
    customers = [
        Customer(
            id=f"CUST-{i:04d}",
            name=f"Cliente Número {i} Pérez González",
            email=f"usuario_{i}@empresa{i % 10}.com",
            phone=f"+52 999 {i:03d} 0000",
            is_active=(i % 2 == 0),
            created_at="2024-01-01T00:00:00Z"
        )
        for i in range(1000)
    ]

    repo = CustomerRepository(data_source=customers)
    service = CustomerSearchService(repository=repo)

    # Medir tiempo de ejecución para búsqueda general
    start_time = time.perf_counter()
    results = service.search(query="perez", field="all")
    elapsed_time = time.perf_counter() - start_time

    # Latencia en milisegundos
    latency_ms = elapsed_time * 1000

    assert len(results) == 1000
    assert latency_ms < 50.0, f"La búsqueda tardó {latency_ms:.2f}ms, superando el límite de 50ms (NFR-01)"


def test_search_latency_filtered_under_50ms():
    """
    Verifica que la búsqueda con filtro de estado activo también cumpla con < 50ms.
    """
    customers = [
        Customer(
            id=f"CUST-{i:04d}",
            name=f"Persona {i} Sánchez",
            email=f"user_{i}@uady.mx",
            is_active=(i % 3 == 0),
            created_at="2024-01-01T00:00:00Z"
        )
        for i in range(1000)
    ]

    repo = CustomerRepository(data_source=customers)
    service = CustomerSearchService(repository=repo)

    start_time = time.perf_counter()
    results = service.search(query="sanchez", field="name", status_filter="active")
    elapsed_time = time.perf_counter() - start_time

    latency_ms = elapsed_time * 1000
    assert len(results) == 334
    assert latency_ms < 50.0, f"La búsqueda filtrada tardó {latency_ms:.2f}ms (límite 50ms)"
