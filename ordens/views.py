from django.shortcuts import render, redirect, get_object_or_404
from .models import OrdemServico, ItemOS
from clientes.models import Cliente
from estoque.models import Peca

def listar_ordens(request):
    # Ordem decrescente por valor total
    ordens = OrdemServico.objects.order_by('-valor_total')
    return render(request, 'ordens/listar.html', {'ordens': ordens})

def adicionar_ordem(request):
    clientes = Cliente.objects.all()
    pecas = Peca.objects.all()
    if request.method == 'POST':
        cliente = Cliente.objects.get(id=request.POST['cliente'])
        ordem = OrdemServico.objects.create(
            cliente=cliente,
            descricao=request.POST['descricao'],
            mao_de_obra=request.POST['mao_de_obra'].replace(',', '.'),
            status=request.POST.get('status', 'aberta')
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
    return render(request, 'ordens/adicionar.html', {'clientes': clientes, 'pecas': pecas})

def editar_ordem(request, id):
    ordem = get_object_or_404(OrdemServico, id=id)
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        ordem.cliente = Cliente.objects.get(id=request.POST['cliente'])
        ordem.descricao = request.POST['descricao']
        ordem.mao_de_obra = request.POST['mao_de_obra'].replace(',', '.')
        ordem.status = request.POST.get('status', 'aberta')
        ordem.save()
        ordem.calcular_total()
        return redirect('listar_ordens')
    return render(request, 'ordens/editar.html', {'ordem': ordem, 'clientes': clientes})

def excluir_ordem(request, id):
    ordem = get_object_or_404(OrdemServico, id=id)
    if request.method == 'POST':
        ordem.delete()
        return redirect('listar_ordens')
    return render(request, 'ordens/confirmar_exclusao.html', {'ordem': ordem})

