import os
 
from dotenv import load_dotenv
 
# Carrega as variáveis do arquivo .env (se existir) para os defaults abaixo.
# Em produção (Render), as variáveis são definidas direto no painel, então
# esse .env não é necessário lá — só facilita o desenvolvimento local.
load_dotenv()
 
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
 
 
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-troque-em-producao")
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"
 
    # Produção: defina DATABASE_URL apontando para o PostgreSQL, ex.:
    #   postgresql+psycopg2://usuario:senha@localhost:5432/nexum
    # Desenvolvimento: sem DATABASE_URL definida, usa SQLite local em instance/,
    # o que evita exigir um PostgreSQL instalado só para rodar o projeto localmente.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'nexum.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
 