# app/routes/gasto.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from app import db
from app.models import Gasto
from app.forms import GastoForm
from datetime import date, timedelta
from werkzeug.utils import secure_filename
import os
import uuid

gasto_bp = Blueprint('gasto', __name__)


def calcular_metricas_gastos():
    """Calcula métricas para o dashboard de gastos"""
    hoje = date.today()
    inicio_mes = hoje.replace(day=1)

    # Total de gastos no mês
    gastos_mes = Gasto.query.filter(
        Gasto.data_gasto >= inicio_mes,
        Gasto.data_gasto <= hoje
    ).all()

    total_mes = sum(g.valor for g in gastos_mes)
    quantidade_mes = len(gastos_mes)

    # Maior categoria
    categorias = {}
    for g in gastos_mes:
        if g.categoria not in categorias:
            categorias[g.categoria] = 0
        categorias[g.categoria] += g.valor

    maior_categoria = max(categorias.items(), key=lambda x: x[1]) if categorias else (None, 0)

    return {
        'total_mes': total_mes,
        'quantidade_mes': quantidade_mes,
        'maior_categoria_nome': maior_categoria[0],
        'maior_categoria_valor': maior_categoria[1],
        'maior_categoria_percentual': (maior_categoria[1] / total_mes * 100) if total_mes > 0 else 0
    }


@gasto_bp.route('/')
def list_gastos():
    """Lista todos os gastos cadastrados"""
    # Filtros
    search = request.args.get('search', '')
    categoria = request.args.get('categoria', 'todos')
    periodo = request.args.get('periodo', 'mes')

    query = Gasto.query

    # Filtro de busca
    if search:
        query = query.filter(
            db.or_(
                Gasto.descricao.ilike(f'%{search}%'),
                Gasto.fornecedor.ilike(f'%{search}%')
            )
        )

    # Filtro de categoria
    if categoria != 'todos':
        query = query.filter(Gasto.categoria == categoria)

    # Filtro de período
    hoje = date.today()
    if periodo == 'mes':
        inicio = hoje.replace(day=1)
        query = query.filter(Gasto.data_gasto >= inicio)
    elif periodo == '30dias':
        inicio = hoje - timedelta(days=30)
        query = query.filter(Gasto.data_gasto >= inicio)

    gastos = query.order_by(Gasto.data_gasto.desc()).all()

    # Calcular métricas
    metricas = calcular_metricas_gastos()

    return render_template(
        'gastos/list.html',
        gastos=gastos,
        metricas=metricas,
        search=search,
        categoria=categoria,
        periodo=periodo
    )


@gasto_bp.route('/novo', methods=['GET', 'POST'])
def create_gasto():
    """Cadastra um novo gasto"""
    form = GastoForm()

    if form.validate_on_submit():
        # Processar upload do comprovante
        comprovante_filename = None
        if form.comprovante.data:
            arquivo = form.comprovante.data
            filename = secure_filename(arquivo.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            arquivo.save(upload_path)
            comprovante_filename = unique_filename

        novo_gasto = Gasto(
            descricao=form.descricao.data,
            categoria=form.categoria.data,
            valor=form.valor.data,
            data_gasto=form.data_gasto.data,
            fornecedor=form.fornecedor.data,
            forma_pagamento=form.forma_pagamento.data,
            observacoes=form.observacoes.data,
            comprovante=comprovante_filename
        )
        db.session.add(novo_gasto)
        db.session.commit()

        flash('Gasto registrado com sucesso!', 'success')
        return redirect(url_for('gasto.list_gastos'))

    # Define data de hoje como padrão
    if request.method == 'GET':
        form.data_gasto.data = date.today()

    # Calcular métricas para o card lateral
    metricas = calcular_metricas_gastos()

    return render_template('gastos/create.html', form=form, metricas=metricas)


@gasto_bp.route('/<int:id>')
def detail_gasto(id):
    """Mostra detalhes de um gasto"""
    gasto = Gasto.query.get_or_404(id)

    # Calcular impacto no mês
    hoje = date.today()
    inicio_mes = hoje.replace(day=1)

    gastos_mes = Gasto.query.filter(
        Gasto.data_gasto >= inicio_mes,
        Gasto.data_gasto <= hoje
    ).all()

    total_mes = sum(g.valor for g in gastos_mes)
    percentual = (gasto.valor / total_mes * 100) if total_mes > 0 else 0

    # Gastos da mesma categoria no mês
    gastos_categoria = [g for g in gastos_mes if g.categoria == gasto.categoria]
    total_categoria = sum(g.valor for g in gastos_categoria)

    return render_template(
        'gastos/detail.html',
        gasto=gasto,
        percentual=percentual,
        total_mes=total_mes,
        total_categoria=total_categoria
    )


@gasto_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def edit_gasto(id):
    """Edita um gasto existente"""
    gasto = Gasto.query.get_or_404(id)
    form = GastoForm(obj=gasto)

    if form.validate_on_submit():
        gasto.descricao = form.descricao.data
        gasto.categoria = form.categoria.data
        gasto.valor = form.valor.data
        gasto.data_gasto = form.data_gasto.data
        gasto.fornecedor = form.fornecedor.data
        gasto.forma_pagamento = form.forma_pagamento.data
        gasto.observacoes = form.observacoes.data

        # Processar novo upload se houver
        if form.comprovante.data:
            arquivo = form.comprovante.data
            filename = secure_filename(arquivo.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            arquivo.save(upload_path)
            gasto.comprovante = unique_filename

        db.session.commit()
        flash('Gasto atualizado com sucesso!', 'success')
        return redirect(url_for('gasto.detail_gasto', id=gasto.id))

    return render_template('gastos/edit.html', form=form, gasto=gasto)


@gasto_bp.route('/<int:id>/excluir', methods=['POST'])
def delete_gasto(id):
    """Exclui um gasto"""
    gasto = Gasto.query.get_or_404(id)

    # Remover arquivo de comprovante se existir
    if gasto.comprovante:
        arquivo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], gasto.comprovante)
        if os.path.exists(arquivo_path):
            os.remove(arquivo_path)

    db.session.delete(gasto)
    db.session.commit()

    flash('Gasto excluído com sucesso!', 'success')
    return redirect(url_for('gasto.list_gastos'))