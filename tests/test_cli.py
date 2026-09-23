"""
Integration tests for Customer Search CLI interface (FR-06, AC-06).
"""

import sys
import pytest
from src.cli import main, format_table
from src.models import Customer


def test_format_table_with_results():
    customers = [
        Customer(id="C-1", name="María Gómez", email="maria@example.com", phone="+52 999 111 2233", is_active=True),
        Customer(id="C-2", name="Carlos López", email="carlos@example.com", phone=None, is_active=False),
    ]
    table = format_table(customers)
    assert "María Gómez" in table
    assert "maria@example.com" in table
    assert "Activo" in table
    assert "Inactivo" in table
    assert "Total de clientes encontrados: 2" in table


def test_format_table_empty():
    table = format_table([])
    assert "No se encontraron clientes que coincidan" in table


def test_cli_search_success(capsys):
    # FR-01, FR-06
    exit_code = main(["--query", "garcia"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Ana Sofía García" in captured.out
    assert "Total de clientes encontrados" in captured.out


def test_cli_search_by_email_only(capsys):
    # FR-02, FR-06
    exit_code = main(["--query", "uady.mx", "--field", "email"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "ana.garcia@uady.mx" in captured.out
    assert "valeria.sanchez@uady.mx" in captured.out


def test_cli_search_active_only_flag(capsys):
    # FR-05, FR-06
    exit_code = main(["--query", "gomez", "--active-only"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "María José Gómez" in captured.out
    assert "Roberto Gómez Bolaños" in captured.out


def test_cli_search_no_matches(capsys):
    exit_code = main(["--query", "NonExistentCustomerName"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "No se encontraron clientes" in captured.out


def test_cli_validation_empty_query_fails(capsys):
    # AC-04: Exit code 2 for validation failure
    exit_code = main(["--query", "  "])
    assert exit_code == 2
    captured = capsys.readouterr()
    assert "Error de validación" in captured.err


def test_cli_validation_short_query_fails(capsys):
    # AC-04: Exit code 2 for query too short
    exit_code = main(["--query", "x"])
    assert exit_code == 2
    captured = capsys.readouterr()
    assert "Error de validación" in captured.err


def test_cli_file_not_found_fails(capsys):
    exit_code = main(["--query", "test", "--json-path", "missing_file.json"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Error de repositorio" in captured.err


def test_cli_interactive_input(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "castillo")
    exit_code = main([])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Fernando Castillo" in captured.out
