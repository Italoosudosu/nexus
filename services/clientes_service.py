"""
NEXUM — services/clientes_service.py
Regras de negócio do CRUD de Clientes. As rotas (routes/clientes.py) apenas
recebem a requisição HTTP e delegam para cá — nenhuma regra de negócio deve
viver na camada de rotas nem no JavaScript do frontend.
"""

import re
import sys
from datetime import datetime
from pathlib import Path

from sqlalchemy import or_

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database import db
from models import Cliente, Endereco


class ValidationError(Exception):
    """Erro de validação de dados — deve virar HTTP 400 na camada de rotas."""

    def __init__(self, mensagem, campo=None):
        self.mensagem = mensagem
        self.campo = campo
        super().__init__(mensagem)


class NotFoundError(Exception):
    """Registro não encontrado — deve virar HTTP 404 na camada de rotas."""


class ConflictError(Exception):
    """Conflito de dados (ex.: CPF duplicado) — deve virar HTTP 409."""


def _apenas_digitos(valor):
    return re.sub(r"\D", "", valor or "")


def _validar_cpf(cpf):
    """Validação de CPF (dígitos verificadores). Retorna o CPF só com dígitos."""
    cpf = _apenas_digitos(cpf)

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido.", campo="cpf")

    for i in [9, 10]:
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]):
            raise ValidationError("CPF inválido.", campo="cpf")

    return cpf


def _formatar_cpf(cpf):
    cpf = _apenas_digitos(cpf)
    return f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"


def _validar_dados(dados, cliente_id=None):
    nome = (dados.get("nome") or "").strip()
    if not nome:
        raise ValidationError("Nome é obrigatório.", campo="nome")

    cpf = _validar_cpf(dados.get("cpf", ""))

    consulta = Cliente.query.filter(Cliente.cpf == cpf)
    if cliente_id:
        consulta = consulta.filter(Cliente.id != cliente_id)
    if consulta.first():
        raise ConflictError("Já existe um cliente cadastrado com este CPF.")

    data_nascimento = None
    if dados.get("data_nascimento"):
        try:
            data_nascimento = datetime.strptime(dados["data_nascimento"], "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("Data de nascimento inválida.", campo="data_nascimento")

    status = dados.get("status", "ativo")
    if status not in ("ativo", "inativo"):
        raise ValidationError("Status inválido.", campo="status")

    return {
        "nome": nome,
        "cpf": cpf,
        "telefone": (dados.get("telefone") or "").strip(),
        "email": (dados.get("email") or "").strip(),
        "data_nascimento": data_nascimento,
        "status": status,
    }


def listar_clientes(busca=None):
    """Lista clientes, opcionalmente filtrando por nome ou CPF."""
    consulta = Cliente.query

    if busca:
        termo = f"%{busca.strip()}%"
        termo_cpf = f"%{_apenas_digitos(busca)}%"
        consulta = consulta.filter(
            or_(Cliente.nome.ilike(termo), Cliente.cpf.ilike(termo_cpf))
        )

    clientes = consulta.order_by(Cliente.nome.asc()).all()
    return [c.to_dict() for c in clientes]


def obter_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        raise NotFoundError(f"Cliente {cliente_id} não encontrado.")
    return cliente


def criar_cliente(dados):
    dados_validados = _validar_dados(dados)

    cliente = Cliente(**dados_validados)

    endereco_dados = dados.get("endereco") or {}
    if any(endereco_dados.values()):
        cliente.endereco = Endereco(
            cep=endereco_dados.get("cep"),
            logradouro=endereco_dados.get("logradouro"),
            numero=endereco_dados.get("numero"),
            complemento=endereco_dados.get("complemento"),
            bairro=endereco_dados.get("bairro"),
            cidade=endereco_dados.get("cidade"),
            estado=endereco_dados.get("estado"),
        )

    db.session.add(cliente)
    db.session.commit()
    return cliente


def atualizar_cliente(cliente_id, dados):
    cliente = obter_cliente(cliente_id)
    dados_validados = _validar_dados(dados, cliente_id=cliente_id)

    for campo, valor in dados_validados.items():
        setattr(cliente, campo, valor)

    endereco_dados = dados.get("endereco") or {}
    if any(endereco_dados.values()):
        if cliente.endereco is None:
            cliente.endereco = Endereco()
        for campo in ("cep", "logradouro", "numero", "complemento", "bairro", "cidade", "estado"):
            setattr(cliente.endereco, campo, endereco_dados.get(campo))

    db.session.commit()
    return cliente


def excluir_cliente(cliente_id):
    cliente = obter_cliente(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
