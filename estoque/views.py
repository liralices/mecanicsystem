from django.shortcuts import render, redirect, get_object_or_404
from .models import Peca

def listar_pecas(request):
    pecas = Peca.objects.all()
    return render(request, 'estoque/listar.html', {'pecas': pecas})

def adicionar_peca(request):
    if request.method == 'POST':
        Peca.objects.create(
            nome=request.POST['nome'],
            quantidade=request.POST['quantidade'],
            estoque_minimo=request.POST.get('estoque_minimo', 5),
            preco_custo=request.POST['preco_custo'].replace(',', '.'),
            preco_venda=request.POST['preco_venda'].replace(',', '.'),
            fornecedor=request.POST['fornecedor']
        )
        return redirect('listar_pecas')
    return render(request, 'estoque/adicionar.html')

def editar_peca(request, id):
    peca = get_object_or_404(Peca, id=id)
    if request.method == 'POST':
        peca.nome = request.POST['nome']
        peca.quantidade = request.POST['quantidade']
        peca.estoque_minimo = request.POST.get('estoque_minimo', 5)
        peca.preco_custo = request.POST['preco_custo'].replace(',', '.')
        peca.preco_venda = request.POST['preco_venda'].replace(',', '.')
        peca.fornecedor = request.POST['fornecedor']
        peca.save()
        return redirect('listar_pecas')
    return render(request, 'estoque/editar.html', {'peca': peca})

def excluir_peca(request, id):
    peca = get_object_or_404(Peca, id=id)
    if request.method == 'POST':
        peca.delete()
        return redirect('listar_pecas')
    return render(request, 'estoque/confirmar_exclusao.html', {'peca': peca})