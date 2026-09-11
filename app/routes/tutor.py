# app/routes/tutor.py
# Rotas CRUD de Tutores

from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Tutor, Pet
from app.forms import TutorForm

tutor_bp = Blueprint('tutor', __name__)


@tutor_bp.route('/')
def list_tutores():
    """Lista todos os tutores cadastrados"""
    tutores = Tutor.query.order_by(Tutor.nome).all()
    total_pets = Pet.query.count()
    return render_template(
        'tutores/list.html',
        tutores=tutores,
        total_pets=total_pets
    )


@tutor_bp.route('/novo', methods=['GET', 'POST'])
def create_tutor():
    """Cadastra um novo tutor"""
    form = TutorForm()
    
    if form.validate_on_submit():
        tutor = Tutor(
            nome=form.nome.data,
            telefone=form.telefone.data,
            email=form.email.data,
            endereco=form.endereco.data,
            observacoes=form.observacoes.data
        )
        db.session.add(tutor)
        db.session.commit()
        
        flash('Tutor cadastrado com sucesso!', 'success')
        return redirect(url_for('tutor.list_tutores'))
    
    return render_template('tutores/create.html', form=form)


@tutor_bp.route('/<int:tutor_id>/editar', methods=['GET', 'POST'])
def edit_tutor(tutor_id):
    """Edita um tutor existente"""
    tutor = Tutor.query.get_or_404(tutor_id)
    form = TutorForm(obj=tutor)
    
    if form.validate_on_submit():
        tutor.nome = form.nome.data
        tutor.telefone = form.telefone.data
        tutor.email = form.email.data
        tutor.endereco = form.endereco.data
        tutor.observacoes = form.observacoes.data
        
        db.session.commit()
        flash('Tutor atualizado com sucesso!', 'success')
        return redirect(url_for('tutor.tutor_profile', tutor_id=tutor.id))
    
    return render_template('tutores/edit.html', form=form, tutor=tutor)


@tutor_bp.route('/<int:tutor_id>')
def tutor_profile(tutor_id):
    """Mostra o perfil detalhado de um tutor"""
    tutor = Tutor.query.get_or_404(tutor_id)
    return render_template('tutores/profile.html', tutor=tutor)