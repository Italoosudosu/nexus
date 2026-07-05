"""
NEXUM — routes/dashboard.py
Rota do painel principal.

Os dados exibidos aqui ainda são mockados: o objetivo desta sprint é validar
o layout (Sidebar + Header + Conteúdo). A partir da Sprint 3/4, as funções
_get_resumo_financeiro() e _get_cobrancas_hoje() serão substituídas por
chamadas a services/ que consultam o banco via SQLAlchemy.
"""

from datetime import date

from flask import Blueprint, render_template

dashboard_bp = Blueprint("dashboard", __name__)


def _get_resumo_financeiro():
    """TODO (Sprint 3/4): substituir por consulta real via services/financeiro.py"""
    return {
        "na_rua": "R$ 10k",
        "a_receber": "R$ 14,6k",
        "em_atraso": "R$ 2.790,00",
        "lucro_mes": "R$ 4,6k",
    }


def _get_cobrancas_hoje():
    """TODO (Sprint 4): substituir por consulta real via services/emprestimos.py"""
    return [
        {
            "nome": "Zenilton",
            "valor": "R$ 910",
            "detalhe": "Venceu 27/06 · 3 dias atraso",
            "status": "atraso",
            "tag": "+R$60,00 multa",
        },
        {
            "nome": "Farley — Renegociação",
            "valor": "R$ 380",
            "detalhe": "Venceu 26/06 · 4 dias atraso",
            "status": "atraso",
            "tag": "+R$80,00 multa",
        },
        {
            "nome": "Farley — Semanal Quinta",
            "valor": "R$ 220",
            "detalhe": "Venceu 25/06 · 5 dias atraso",
            "status": "atraso",
            "tag": "+R$100,00 multa",
        },
        {
            "nome": "Ademir — Domingo",
            "valor": "R$ 360",
            "detalhe": "Vence hoje às 18h",
            "status": "hoje",
            "tag": "vence hoje",
        },
        {
            "nome": "Zieliton — Play 4",
            "valor": "R$ 160",
            "detalhe": "Parcela pendente · vence hoje",
            "status": "hoje",
            "tag": "vence hoje",
        },
        {
            "nome": "Lucas — Segunda",
            "valor": "R$ 660",
            "detalhe": "Vence amanhã 01/07",
            "status": "amanha",
            "tag": "amanhã",
        },
    ]


@dashboard_bp.route("/dashboard")
def index():
    """Renderiza o painel principal com o resumo financeiro e cobranças do dia."""
    contexto = {
        "usuario_nome": "Fernando",
        "resumo": _get_resumo_financeiro(),
        "alerta": {"clientes_atraso": 3, "multas_total": "R$120,00"},
        "cobrancas": _get_cobrancas_hoje(),
        "data_hoje": date.today().strftime("%d/%m/%Y"),
    }
    return render_template("dashboard.html", **contexto)
