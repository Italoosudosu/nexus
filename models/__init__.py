"""
NEXUM — models/__init__.py
Reexporta os models para permitir `from models import Cliente, Endereco`
e garante que ambos sejam registrados no metadata do SQLAlchemy quando
este pacote for importado (necessário para o Flask-Migrate detectá-los).
"""

from models.cliente import Cliente
from models.endereco import Endereco

__all__ = ["Cliente", "Endereco"]
