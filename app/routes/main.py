# app/routes/main.py
from flask import Blueprint, render_template
from app.models import Tutor, Pet, Atendimento, Gasto
from datetime import date, datetime

main_bp = Blueprint('main', __name__)

# Meses em português (Jinja não tem locale nativo confiável no Windows)
MESES_PT = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}

@main_bp.route('/')
def index():
    hoje = date.today()
    inicio_mes = hoje.replace(day=1)

    # Saudação por período do dia
    hora = datetime.now().hour
    if hora < 12:
        saudacao = 'Bom dia'
    elif hora < 18:
        saudacao = 'Boa tarde'
    else:
        saudacao = 'Boa noite'

    # Data formatada em português
    data_formatada = f"{hoje.day} de {MESES_PT[hoje.month]} de {hoje.year}"

    # KPIs de cadastro
    total_tutores = Tutor.query.count()
    total_pets = Pet.query.count()

    # KPIs financeiros do mês
    atendimentos_mes = Atendimento.query.filter(Atendimento.data_atendimento >= inicio_mes).all()
    gastos_mes = Gasto.query.filter(Gasto.data_gasto >= inicio_mes).all()

    faturamento_mes = sum(a.valor for a in atendimentos_mes)
    total_gastos_mes = sum(g.valor for g in gastos_mes)
    lucro_mes = faturamento_mes - total_gastos_mes

    # Últimos atendimentos (para a lista rápida)
    atendimentos_recentes = Atendimento.query.order_by(
        Atendimento.data_atendimento.desc()
    ).limit(5).all()

    return render_template(
        'index.html',
        saudacao=saudacao,
        data_formatada=data_formatada,
        total_tutores=total_tutores,
        total_pets=total_pets,
        total_atendimentos_mes=len(atendimentos_mes),
        faturamento_mes=faturamento_mes,
        total_gastos_mes=total_gastos_mes,
        lucro_mes=lucro_mes,
        atendimentos_recentes=atendimentos_recentes
    )