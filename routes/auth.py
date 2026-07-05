"""
NEXUM — routes/auth.py
Rotas de autenticação. Nesta sprint apenas exibem a tela de login;
a validação de credenciais (Flask-Login) entra quando o backend de
usuários for implementado.
"""

from flask import Blueprint, render_template

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
@auth_bp.route("/login")
def login():
    """Exibe a tela de autenticação."""
    return render_template("login.html")