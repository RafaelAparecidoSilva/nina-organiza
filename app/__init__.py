# app/__init__.py
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import config
import os

# Inicializar extensões ANTES dos imports dos blueprints
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_name='default'):
    """Cria e configura o aplicativo Flask"""
    app = Flask(__name__)

    # Carrega configuração
    app.config.from_object(config[config_name])

    # Inicializa extensões com o app
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Cria pasta de uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # IMPORTA OS BLUEPRINTS DENTRO DA FUNÇÃO (isso resolve o circular import)
    from app.routes.tutor import tutor_bp
    from app.routes.pet import pet_bp
    from app.routes.atendimento import atendimento_bp
    from app.routes.gasto import gasto_bp

    # Registra os blueprints
    app.register_blueprint(tutor_bp, url_prefix='/tutores')
    app.register_blueprint(pet_bp, url_prefix='/pets')
    app.register_blueprint(atendimento_bp, url_prefix='/atendimentos')
    app.register_blueprint(gasto_bp, url_prefix='/gastos')

    # Rota raiz (redireciona para lista de tutores)
    @app.route('/')
    def index():
        return redirect(url_for('tutor.list_tutores'))

    return app