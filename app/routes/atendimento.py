# app/routes/atendimento.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Atendimento, Pet, Tutor
from app.forms import AtendimentoForm
from datetime import date

atendimento_bp = Blueprint('atendimento', __name__)

@atendimento_bp.route('/')
def list_atendimentos():
    # Busca todos os atendimentos, ordenando do mais recente para o mais antigo
    atendimentos = Atendimento.query.order_by(Atendimento.data_atendimento.desc()).all()
    return render_template('atendimentos/list.html', atendimentos=atendimentos)

@atendimento_bp.route('/novo', methods=['GET', 'POST'])
def create_atendimento():
    form = AtendimentoForm()
    
    # Popula o dropdown com os pets cadastrados (Mostrando Nome do Pet - Nome do Tutor)
    form.pet_id.choices = [
        (p.id, f"{p.nome} (Tutor: {p.tutor.nome})") 
        for p in Pet.query.order_by(Pet.nome).all()
    ]
    
    if form.validate_on_submit():
        novo_atendimento = Atendimento(
            pet_id=form.pet_id.data,
            servico=form.servico.data,
            valor=form.valor.data,
            data_atendimento=form.data_atendimento.data,
            forma_pagamento=form.forma_pagamento.data,
            observacoes=form.observacoes.data,
            produtos_utilizados=form.produtos_utilizados.data
        )
        db.session.add(novo_atendimento)
        db.session.commit()
        flash('Atendimento registrado com sucesso!', 'success')
        return redirect(url_for('atendimento.list_atendimentos'))
        
    # Define a data de hoje como padrão no formulário
    if request.method == 'GET':
        form.data_atendimento.data = date.today()
        
    return render_template('atendimentos/create.html', form=form)

@atendimento_bp.route('/<int:id>')
def detail_atendimento(id):
    atendimento = Atendimento.query.get_or_404(id)
    return render_template('atendimentos/detail.html', atendimento=atendimento)