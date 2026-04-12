from django.shortcuts import render, redirect
from .models import OrdemServico, ItemOS
from clientes.models import Cliente
from estoque.models import Peca

def listar_ordens(request):
    ordens = OrdemServico.objects.all()
    return render(request, 'ordens/listar.html', {'ordens': ordens})

def adicionar_ordem(request):
    clientes = Cliente.objects.all()
    pecas = Peca.objects.all()
    if request.method == 'POST':
        cliente = Cliente.objects.get(id=request.POST['cliente'])
        ordem = OrdemServico.objects.create(
            cliente=cliente,
            descricao=request.POST['descricao'],
            mao_de_obra=request.POST['mao_de_obra']
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
