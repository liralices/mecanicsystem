from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from clientes.models import Cliente
from estoque.models import Peca
from ordens.models import OrdemServico
from configuracoes.models import ConfiguracaoOficina
from datetime import date, timedelta

def home(request):
    hoje = date.today()
    inicio_mes = hoje.replace(day=1)

    # Configuração da Oficina
    try:
        config = ConfiguracaoOficina.objects.first()
        if not config:
            config = ConfiguracaoOficina.objects.create()
    except:
        config = None

    # Indicadores de clientes
    total_clientes = Cliente.objects.count()
    clientes_novos = Cliente.objects.filter(
        id__gte=Cliente.objects.order_by('-id').first().id - 5
    ).count() if Cliente.objects.exists() else 0

    # Indicadores de OS
    total_os_mes = OrdemServico.objects.filter(data__gte=inicio_mes).count()
    os_abertas = OrdemServico.objects.filter(status='aberta').count()
    os_andamento = OrdemServico.objects.filter(status='em_andamento').count()
    os_aguardando = OrdemServico.objects.filter(status='aguardando_peca').count()
    os_concluidas = OrdemServico.objects.filter(
        status='concluida', data__gte=inicio_mes
    ).count()

    # Faturamento
    faturamento_mes = OrdemServico.objects.filter(
        data__gte=inicio_mes, status='concluida'
    ).aggregate(total=Sum('valor_total'))['total'] or 0

    receita_mao_obra = OrdemServico.objects.filter(
        data__gte=inicio_mes, status='concluida'
    ).aggregate(total=Sum('mao_de_obra'))['total'] or 0

    receita_pecas = faturamento_mes - receita_mao_obra

    ticket_medio = (faturamento_mes / os_concluidas) if os_concluidas > 0 else 0

    # Indicadores de estoque
    total_pecas = Peca.objects.count()
    pecas_baixo_estoque = Peca.objects.filter(quantidade__lte=5)
    alertas_estoque = pecas_baixo_estoque.count()

    # OS recentes
    os_recentes = OrdemServico.objects.order_by('-id')[:5]

    context = {
        'config': config,
        'total_clientes': total_clientes,
        'total_os_mes': total_os_mes,
        'os_abertas': os_abertas,
        'os_andamento': os_andamento,
        'os_aguardando': os_aguardando,
        'os_concluidas': os_concluidas,
        'faturamento_mes': faturamento_mes,
        'receita_mao_obra': receita_mao_obra,
        'receita_pecas': receita_pecas,
        'ticket_medio': ticket_medio,
        'total_pecas': total_pecas,
        'alertas_estoque': alertas_estoque,
        'pecas_baixo_estoque': pecas_baixo_estoque,
        'os_recentes': os_recentes,
    }

    return render(request, 'home.html', context)
