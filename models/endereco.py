"""
NEXUM — models/endereco.py
Endereço do cliente. Relação 1-para-1 com Cliente: cada cliente possui
um único endereço residencial cadastrado nesta etapa do projeto.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database import db


class Endereco(db.Model):
    __tablename__ = "enderecos"

    id = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.String(9))
    logradouro = db.Column(db.String(150))
    numero = db.Column(db.String(15))
    complemento = db.Column(db.String(80))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))

    cliente_id = db.Column(
        db.Integer, db.ForeignKey("clientes.id"), unique=True, nullable=False
    )

    def to_dict(self):
        return {
            "cep": self.cep,
            "logradouro": self.logradouro,
            "numero": self.numero,
            "complemento": self.complemento,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "estado": self.estado,
        }
