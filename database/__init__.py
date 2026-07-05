"""
NEXUM — database/__init__.py
Instância única do SQLAlchemy, compartilhada por toda a aplicação.

Mantida em módulo separado (em vez de dentro de app.py) para evitar
importação circular: models/ importa `db` daqui, e app.py importa os
models e o `db` sem depender um do outro diretamente.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
