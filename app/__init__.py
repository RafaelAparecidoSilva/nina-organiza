# app/__init__.py
# Factory do aplicativo Flask

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import config

# Extensões (inicializadas sem app)
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_name='default'):
    """Cria e configura o aplicativo Flask"""
    app = Flask(__name__)
    
    # Carrega configuração
    app.config.from_object(config[config_name])
    
    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Cria pasta de uploads se não existir
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Registra Blueprints (rotas)
    from app.routes.tutor import tutor_bp
    from app.routes.pet import pet_bp
    
    app.register_blueprint(tutor_bp, url_prefix='/tutores')
    app.register_blueprint(pet_bp, url_prefix='/pets')
    
    # Rota raiz (redireciona para lista de tutores)
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('tutor.list_tutores'))
    
    return app