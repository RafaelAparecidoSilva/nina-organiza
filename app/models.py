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
    foto = db.Column(db.String(200), nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Pet {self.nome}>'


class Atendimento(db.Model):
    __tablename__ = 'atendimentos'

    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    servico = db.Column(db.String(100), nullable=False)  # ex: Banho & Tosa
    valor = db.Column(db.Float, nullable=False)
    data_atendimento = db.Column(db.Date, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)  # Pix, Dinheiro, etc.
    observacoes = db.Column(db.Text, nullable=True)
    produtos_utilizados = db.Column(db.Text, nullable=True)  # Ex: "Shampoo X, Condicionador Y"
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento para facilitar o acesso aos dados do Pet/Tutor no template
    pet = db.relationship('Pet', backref=db.backref('atendimentos', lazy=True))


class Gasto(db.Model):
    __tablename__ = 'gastos'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # insumos, equipamentos, manutencao, custos_fixos, outros
    valor = db.Column(db.Float, nullable=False)
    data_gasto = db.Column(db.Date, nullable=False)
    fornecedor = db.Column(db.String(100), nullable=True)
    forma_pagamento = db.Column(db.String(50), nullable=False)  # pix, credito, debito, boleto, dinheiro
    observacoes = db.Column(db.Text, nullable=True)
    comprovante = db.Column(db.String(200), nullable=True)  # nome do arquivo de upload
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Gasto {self.descricao}>'