"""
NEXUM — init_db.py
Cria as tabelas no banco de dados a partir dos models atuais.

USO:
    python init_db.py

Reaproveita a mesma configuração do app (config.py / DATABASE_URL), então
respeita o banco definido na variável de ambiente, exatamente como o
`flask db upgrade` faria.

⚠️ IMPORTANTE — leia antes de usar em produção:
Este script usa db.create_all(), que cria apenas as tabelas que ainda não
existem. Ele NÃO altera tabelas já existentes (não adiciona colunas novas,
não muda tipos, etc.). Serve bem para a criação inicial do banco.

Quando o projeto já tiver dados reais salvos (clientes, empréstimos) e for
necessário mudar um model (adicionar campo, renomear coluna...), use o
fluxo de migrations de verdade, que preserva os dados existentes:

    flask --app app db migrate -m "descreva a mudança aqui"
    flask --app app db upgrade
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from database import db

# Importa os models para que fiquem registrados no metadata do SQLAlchemy
# antes do create_all() rodar.
from models import Cliente, Endereco  # noqa: F401

app = create_app()

with app.app_context():
    db.create_all()
    print("Tabelas criadas com sucesso (ou já existiam).")
