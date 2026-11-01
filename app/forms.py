# app/forms.py
# Formulários WTForms para validação de dados

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, EmailField
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired, Email, Optional, Length
from flask_wtf.file import FileField, FileAllowed

class TutorForm(FlaskForm):
    """Formulário de cadastro de Tutor"""
    nome = StringField('Nome Completo', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=3, max=100, message='Nome deve ter entre 3 e 100 caracteres')
    ])
    telefone = StringField('Telefone', validators=[
        DataRequired(message='Telefone é obrigatório'),
        Length(min=10, max=20, message='Telefone inválido')
    ])
    email = EmailField('E-mail', validators=[
        Optional(),
        Email(message='E-mail inválido')
    ])
    endereco = StringField('Endereço', validators=[
        Optional(),
        Length(max=200, message='Endereço muito longo')
    ])
    observacoes = TextAreaField('Observações', validators=[
        Optional(),
        Length(max=500, message='Observações muito longas (máx. 500 caracteres)')
    ])


class PetForm(FlaskForm):
    """Formulário de cadastro de Pet"""
    nome = StringField('Nome do Pet', validators=[
        DataRequired(message='Nome do pet é obrigatório'),
        Length(min=2, max=50, message='Nome deve ter entre 2 e 50 caracteres')
    ])
    tutor_id = SelectField('Tutor Responsável', coerce=int, validators=[
        DataRequired(message='Selecione um tutor')
    ])
    especie = SelectField('Espécie', choices=[
        ('cao', 'Cão'),
        ('gato', 'Gato')
    ], validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[
        ('macho', 'Macho'),
        ('femea', 'Fêmea')
    ], validators=[DataRequired()])
    raca = StringField('Raça', validators=[
        Optional(),
        Length(max=50, message='Raça muito longa')
    ])
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[
        Optional()
    ])
    porte = SelectField('Porte', choices=[
        ('pequeno', 'Pequeno (até 10kg)'),
        ('medio', 'Médio (10 a 25kg)'),
        ('grande', 'Grande (acima de 25kg)')
    ], validators=[DataRequired()])
    pelagem = SelectField('Tipo de Pelagem', choices=[
        ('curta', 'Curta'),
        ('media', 'Média'),
        ('longa', 'Longa')
    ], validators=[Optional()])
    observacoes = TextAreaField('Observações/Alergias', validators=[
        Optional(),
        Length(max=500, message='Observações muito longas (máx. 500 caracteres)')
    ])
    foto = FileField('Foto do Pet', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens JPG, JPEG ou PNG!')
    ])

class AtendimentoForm(FlaskForm):
    pet_id = SelectField('Pet Atendido', coerce=int, validators=[DataRequired()])
    servico = SelectField('Tipo de Serviço', choices=[
        ('banho', 'Banho Simples'),
        ('tosa-completa', 'Tosa Completa'),
        ('banho-tosa', 'Banho + Tosa'),
        ('tosa-higienica', 'Tosa Higiênica'),
        ('hidratacao', 'Hidratação'),
        ('corte-unhas', 'Corte de Unhas')
    ], validators=[DataRequired()])
    valor = FloatField('Valor Cobrado (R$)', validators=[DataRequired()])
    data_atendimento = DateField('Data do Atendimento', format='%Y-%m-%d', validators=[DataRequired()])
    forma_pagamento = SelectField('Forma de Pagamento', choices=[
        ('pix', 'Pix'),
        ('debito', 'Cartão de Débito'),
        ('credito', 'Cartão de Crédito'),
        ('dinheiro', 'Dinheiro'),
        ('a-receber', 'A Receber')
    ], validators=[DataRequired()])
    observacoes = TextAreaField('Observações do Atendimento', validators=[Optional()])
    produtos_utilizados = TextAreaField('Produtos Utilizados (separados por vírgula)', validators=[Optional()])