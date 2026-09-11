# app/forms.py
# Formulários WTForms para validação de dados

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, EmailField
from wtforms.validators import DataRequired, Email, Optional, Length

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