"""
NEXUM — models/cliente.py
Entidade Cliente. Representa o tomador de crédito.
"""

import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database import db
from models.endereco import Endereco


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(150))
    data_nascimento = db.Column(db.Date)
    status = db.Column(db.String(10), nullable=False, default="ativo")  # ativo | inativo

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    endereco = db.relationship(
        "Endereco",
        backref="cliente",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "telefone": self.telefone,
            "email": self.email,
            "data_nascimento": self.data_nascimento.isoformat() if self.data_nascimento else None,
            "status": self.status,
            "endereco": self.endereco.to_dict() if self.endereco else None,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }





