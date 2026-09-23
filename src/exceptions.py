"""
Domain exceptions for Customer Search.
"""


class CustomerSearchError(Exception):
    """Excepción base para todos los errores del dominio Customer Search."""
    pass


class ValidationError(CustomerSearchError):
    """Excepción base para errores de validación de entradas de búsqueda."""
    pass


class EmptyQueryError(ValidationError):
    """Lanzada cuando el término de búsqueda está vacío o contiene solo espacios."""
    pass


class QueryTooShortError(ValidationError):
    """Lanzada cuando el término de búsqueda tiene menos de 2 caracteres significativos."""
    pass


class InvalidFieldError(ValidationError):
    """Lanzada cuando el campo de búsqueda especificado no es válido."""
    pass


class InvalidStatusFilterError(ValidationError):
    """Lanzada cuando el filtro de estado de cliente no es reconocido."""
    pass


class CustomerRepositoryError(CustomerSearchError):
    """Lanzada ante fallos de persistencia o lectura en el repositorio de datos."""
    pass
