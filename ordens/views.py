from django.shortcuts import render, redirect, get_object_or_404
from .models import OrdemServico, ItemOS
from clientes.models import Cliente, Veiculo
from estoque.models import Peca
from decimal import Decimal

def listar_ordens(request):
    ordens = OrdemServico.objects.order_by('-valor_total')
    return render(request, 'ordens/listar.html', {'ordens': ordens})

def adicionar_ordem(request):
    clientes = Cliente.objects.all()
    pecas = Peca.objects.all().order_by('nome')
    veiculos = Veiculo.objects.all()
    if request.method == 'POST':
        cliente = Cliente.objects.get(id=request.POST['cliente'])
        veiculo_id = request.POST.get('veiculo')
        veiculo = None
        if veiculo_id:
            veiculo = Veiculo.objects.get(id=veiculo_id)
        mao_de_obra = Decimal(request.POST['mao_de_obra'].replace(',', '.'))
        concluida = request.POST.get('concluida') == 'on'
        ordem = OrdemServico.objects.create(
            cliente=cliente,
            veiculo=veiculo,
            descricao=request.POST['descricao'],
            mao_de_obra=mao_de_obra,
            status=request.POST.get('status', 'aberta'),
            concluida=concluida
        )
        for peca in pecas:
            qtd = request.POST.get(f'peca_{peca.id}')
            if qtd and int(qtd) > 0:
                ItemOS.objects.create(
                    ordem_servico=ordem,
                    peca=peca,
                    quantidade=int(qtd)
                )
        ordem.calcular_total()
        return redirect('listar_ordens')
    return render(request, 'ordens/adicionar.html', {'clientes': clientes, 'pecas': pecas, 'veiculos': veiculos})

def editar_ordem(request, id):
    ordem = get_object_or_404(OrdemServico, id=id)
    clientes = Cliente.objects.all()
    veiculos = Veiculo.objects.all()
    if request.method == 'POST':
        ordem.cliente = Cliente.objects.get(id=request.POST['cliente'])
        veiculo_id = request.POST.get('veiculo')
        ordem.veiculo = None
        if veiculo_id:
            ordem.veiculo = Veiculo.objects.get(id=veiculo_id)
        ordem.descricao = request.POST['descricao']
        ordem.mao_de_obra = Decimal(request.POST['mao_de_obra'].replace(',', '.'))
        ordem.status = request.POST.get('status', 'aberta')
        ordem.concluida = request.POST.get('concluida') == 'on'
        ordem.save()
        ordem.calcular_total()
        return redirect('listar_ordens')
    return render(request, 'ordens/editar.html', {'ordem': ordem, 'clientes': clientes, 'veiculos': veiculos})

def excluir_ordem(request, id):
    ordem = get_object_or_404(OrdemServico, id=id)
    if request.method == 'POST':
        ordem.delete()
        return redirect('listar_ordens')
    return render(request, 'ordens/confirmar_exclusao.html', {'ordem': ordem})

from django.http import JsonResponse

def toggle_concluida(request, id):
    if request.method == 'POST':
        ordem = get_object_or_404(OrdemServico, id=id)
        ordem.concluida = not ordem.concluida
        ordem.save()
        return JsonResponse({'concluida': ordem.concluida})
    return JsonResponse({'error': 'Método não permitido'}, status=405)


