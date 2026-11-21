# app/routes/dashboard.py
from flask import Blueprint, render_template
from app.models import Tutor, Pet, Atendimento, Gasto
from datetime import date

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def index():
    hoje = date.today()
    inicio_mes = hoje.replace(day=1)
    mes_atual = hoje.strftime('%B/%Y').capitalize()

    # 1. Métricas de Cadastro
    total_tutores = Tutor.query.count()
    total_pets = Pet.query.count()

    # 2. Métricas de Atendimentos (Receita) do Mês
    atendimentos_mes = Atendimento.query.filter(Atendimento.data_atendimento >= inicio_mes).all()
    faturamento_mes = sum(att.valor for att in atendimentos_mes)
    total_atendimentos_mes = len(atendimentos_mes)

    # Ticket médio (evita divisão por zero)
    ticket_medio = (faturamento_mes / total_atendimentos_mes) if total_atendimentos_mes > 0 else 0.0

    # 3. Métricas de Gastos (Despesa) do Mês
    gastos_mes = Gasto.query.filter(Gasto.data_gasto >= inicio_mes).all()
    total_gastos_mes = sum(g.valor for g in gastos_mes)

    # 4. Lucro Líquido
    lucro_liquido = faturamento_mes - total_gastos_mes

    # 5. Atendimentos Recentes (Últimos 5)
    atendimentos_recentes = Atendimento.query.order_by(Atendimento.data_atendimento.desc()).limit(5).all()

    # 6. Pets Mais Atendidos (Top 3)
    pets_count = {}
    for att in atendimentos_mes:
        nome_pet = att.pet.nome
        pets_count[nome_pet] = pets_count.get(nome_pet, 0) + 1

    pets_mais_atendidos = sorted(pets_count.items(), key=lambda x: x[1], reverse=True)[:3]

    # 7. Gastos por Categoria (para as barras de progresso)
    categorias_gasto = {}
    for g in gastos_mes:
        cat = g.categoria
        categorias_gasto[cat] = categorias_gasto.get(cat, 0.0) + g.valor

    return render_template(
        'dashboard/index.html',
        mes_atual=mes_atual,
        total_tutores=total_tutores,
        total_pets=total_pets,
        faturamento_mes=faturamento_mes,
        total_gastos_mes=total_gastos_mes,
        lucro_liquido=lucro_liquido,
        total_atendimentos_mes=total_atendimentos_mes,
        ticket_medio=ticket_medio,
        atendimentos_recentes=atendimentos_recentes,
        pets_mais_atendidos=pets_mais_atendidos,
        categorias_gasto=categorias_gasto
    )