# app/models.py
# Modelos do banco de dados (SQLAlchemy)

from app import db
from datetime import datetime


class Tutor(db.Model):
    """Modelo de Tutor (cliente do groomer)"""
    __tablename__ = 'tutores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    endereco = db.Column(db.String(200), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento 1:N com Pets
    pets = db.relationship('Pet', backref='tutor', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Tutor {self.nome}>'


class Pet(db.Model):
    """Modelo de Pet"""
    __tablename__ = 'pets'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutores.id'), nullable=False)
    especie = db.Column(db.String(20), default='cao')  # cao, gato
    sexo = db.Column(db.String(10), default='macho')    # macho, femea
    raca = db.Column(db.String(50), nullable=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    porte = db.Column(db.String(10), default='medio')   # pequeno, medio, grande
    pelagem = db.Column(db.String(20), nullable=True)   # curta, media, longa
    observacoes = db.Column(db.Text, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Pet {self.nome}>'