# config.py
# Configurações do projeto NinaOrganiza

import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuração base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-padrao-nina'
    
    # URL do banco de dados (PostgreSQL ou SQLite como fallback)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'nina_organiza.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload de arquivos
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB


class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True


class TestingConfig(Config):
    """Configuração de testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False


# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}