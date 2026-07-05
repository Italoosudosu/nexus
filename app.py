"""
NEXUM — app.py
Ponto de entrada da aplicação Flask.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from flask import Flask
from flask_migrate import Migrate

from config import Config
from database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    # Importa os models para que sejam registrados no metadata do SQLAlchemy
    from models import Cliente, Endereco  # noqa: F401

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.clientes import clientes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(clientes_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])