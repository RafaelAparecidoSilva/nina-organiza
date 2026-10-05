# app/routes/pet.py
# Rotas CRUD de Pets

from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import Pet, Tutor
from app.forms import PetForm
import os
from werkzeug.utils import secure_filename
from flask import current_app

pet_bp = Blueprint('pet', __name__)


@pet_bp.route('/')
def list_pets():
    """Lista todos os pets cadastrados"""
    pets = Pet.query.order_by(Pet.nome).all()
    return render_template('pets/list.html', pets=pets)


@pet_bp.route('/novo', methods=['GET', 'POST'])
def create_pet():
    """Cadastra um novo pet"""
    form = PetForm()
    
    # Popula o dropdown de tutores
    form.tutor_id.choices = [
        (t.id, t.nome) for t in Tutor.query.order_by(Tutor.nome).all()
    ]
    
    if form.validate_on_submit():
        # Processar upload da foto
        foto_filename = None
        if form.foto.data:
            foto = form.foto.data
            filename = secure_filename(foto.filename)

            # Gerar nome único para evitar conflitos
            import uuid
            unique_filename = f"{uuid.uuid4().hex}_{filename}"

            # Salvar na pasta de uploads
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            foto.save(upload_path)
            foto_filename = unique_filename

        pet = Pet(
            nome=form.nome.data,
            tutor_id=form.tutor_id.data,
            especie=form.especie.data,
            sexo=form.sexo.data,
            raca=form.raca.data,
            data_nascimento=form.data_nascimento.data,
            porte=form.porte.data,
            pelagem=form.pelagem.data,
            observacoes=form.observacoes.data,
            foto=foto_filename
        )
        db.session.add(pet)
        db.session.commit()
        
        flash('Pet cadastrado com sucesso!', 'success')
        return redirect(url_for('pet.list_pets'))
    
    return render_template('pets/create.html', form=form)


@pet_bp.route('/<int:pet_id>/editar', methods=['GET', 'POST'])
def edit_pet(pet_id):
    """Edita um pet existente"""
    pet = Pet.query.get_or_404(pet_id)
    form = PetForm(obj=pet)
    
    # Popula o dropdown de tutores
    form.tutor_id.choices = [
        (t.id, t.nome) for t in Tutor.query.order_by(Tutor.nome).all()
    ]
    
    if form.validate_on_submit():
        pet.nome = form.nome.data
        pet.tutor_id = form.tutor_id.data
        pet.especie = form.especie.data
        pet.sexo = form.sexo.data
        pet.raca = form.raca.data
        pet.data_nascimento = form.data_nascimento.data
        pet.porte = form.porte.data
        pet.pelagem = form.pelagem.data
        pet.observacoes = form.observacoes.data
        
        db.session.commit()
        flash('Pet atualizado com sucesso!', 'success')
        return redirect(url_for('pet.pet_profile', pet_id=pet.id))
    
    return render_template('pets/edit.html', form=form, pet=pet)


@pet_bp.route('/<int:pet_id>')
def pet_profile(pet_id):
    """Mostra o prontuário detalhado de um pet"""
    pet = Pet.query.get_or_404(pet_id)
    return render_template('pets/profile.html', pet=pet)