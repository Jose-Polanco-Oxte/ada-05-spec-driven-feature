"""
Command Line Interface (CLI) for Customer Search.
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path
from typing import List, Optional

from src.models import Customer
from src.repository import CustomerRepository
from src.search_service import CustomerSearchService
from src.exceptions import ValidationError, CustomerRepositoryError


def format_table(customers: List[Customer]) -> str:
    """
    Formatea una lista de clientes en una tabla ASCII limpia y legible.
    """
    if not customers:
        return "No se encontraron clientes que coincidan con los criterios de búsqueda.\n"

    headers = ["ID", "Nombre", "Correo Electrónico", "Teléfono", "Estado"]
    rows = []
    for c in customers:
        status_label = "Activo" if c.is_active else "Inactivo"
        phone_label = c.phone or "-"
        rows.append([c.id, c.name, c.email, phone_label, status_label])

    # Calcular ancho de cada columna
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    # Construir líneas
    separator = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    header_line = "| " + " | ".join(h.ljust(w) for h, w in zip(headers, col_widths)) + " |"

    data_lines = []
    for row in rows:
        data_lines.append("| " + " | ".join(cell.ljust(w) for cell, w in zip(row, col_widths)) + " |")

    table_lines = [
        separator,
        header_line,
        separator,
        *data_lines,
        separator,
        f"Total de clientes encontrados: {len(customers)}\n"
    ]
    return "\n".join(table_lines)


def build_parser() -> argparse.ArgumentParser:
    """Configura el parser de argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        prog="customer-search",
        description="Búsqueda de clientes por nombre, correo o término general con soporte para acentos y coincidencias parciales."
    )
    parser.add_argument(
        "-q", "--query",
        type=str,
        help="Término de búsqueda (mínimo 2 caracteres). Si se omite, se solicitará de forma interactiva."
    )
    parser.add_argument(
        "-f", "--field",
        choices=["all", "name", "email"],
        default="all",
        help="Campo sobre el cual buscar: 'all' (nombre o correo), 'name' (solo nombre), 'email' (solo correo). Por defecto: all."
    )
    parser.add_argument(
        "-s", "--status",
        choices=["all", "active", "inactive"],
        default="all",
        help="Filtrar por estado del cliente: 'all', 'active', 'inactive'. Por defecto: all."
    )
    parser.add_argument(
        "--active-only",
        action="store_true",
        help="Atajo para filtrar exclusivamente clientes activos (equivalente a --status active)."
    )
    parser.add_argument(
        "-j", "--json-path",
        type=str,
        default=None,
        help="Ruta personalizada al archivo de clientes en formato JSON (por defecto: data/customers.json)."
    )
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """
    Punto de entrada principal para la CLI de Customer Search.
    Retorna código de salida numérico: 0 = éxito, 1 = error de sistema/datos, 2 = error de validación.
    """
    parser = build_parser()
    parsed_args = parser.parse_args(args)

    query = parsed_args.query
    if query is None:
        # Modo interactivo si no se proporcionó por bandera
        try:
            query = input("Ingrese el término de búsqueda de clientes: ")
        except (EOFError, KeyboardInterrupt):
            print("\nOperación cancelada.", file=sys.stderr)
            return 2

    status_filter = "active" if parsed_args.active_only else parsed_args.status

    try:
        repo = CustomerRepository(data_source=parsed_args.json_path)
        service = CustomerSearchService(repository=repo)
        results = service.search(
            query=query,
            field=parsed_args.field,
            status_filter=status_filter
        )
        print(format_table(results))
        return 0

    except ValidationError as err:
        print(f"Error de validación: {err}", file=sys.stderr)
        return 2

    except CustomerRepositoryError as err:
        print(f"Error de repositorio: {err}", file=sys.stderr)
        return 1

    except Exception as err:
        print(f"Error inesperado: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
