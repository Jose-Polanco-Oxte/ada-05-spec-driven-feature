"""
Unit tests for Customer domain model.
"""

import pytest
from src.models import Customer


def test_customer_creation_valid():
    customer = Customer(
        id="CUST-001",
        name="María José Gómez",
        email="maria@example.com",
        phone="+52 999 123 4567",
        is_active=True,
        created_at="2024-01-01T00:00:00Z"
    )
    assert customer.id == "CUST-001"
    assert customer.name == "María José Gómez"
    assert customer.email == "maria@example.com"
    assert customer.phone == "+52 999 123 4567"
    assert customer.is_active is True
    assert customer.created_at == "2024-01-01T00:00:00Z"


def test_customer_is_immutable():
    customer = Customer(id="CUST-001", name="Test", email="test@mail.com")
    with pytest.raises(Exception):
        customer.name = "Modified"  # frozen dataclass prohibits assignment


def test_customer_validation_empty_id():
    with pytest.raises(ValueError, match="El 'id' del cliente no puede estar vacío."):
        Customer(id="", name="Test", email="test@mail.com")


def test_customer_validation_empty_name():
    with pytest.raises(ValueError, match="El 'name' del cliente no puede estar vacío."):
        Customer(id="CUST-001", name="   ", email="test@mail.com")


def test_customer_validation_empty_email():
    with pytest.raises(ValueError, match="El 'email' del cliente no puede estar vacío."):
        Customer(id="CUST-001", name="Test", email="")


def test_customer_from_and_to_dict():
    raw_data = {
        "id": "CUST-002",
        "name": "Carlos Pérez",
        "email": "carlos@example.com",
        "phone": None,
        "is_active": False,
        "created_at": "2024-02-01T12:00:00Z"
    }
    customer = Customer.from_dict(raw_data)
    assert customer.id == "CUST-002"
    assert customer.name == "Carlos Pérez"
    assert customer.is_active is False
    assert customer.to_dict() == raw_data
