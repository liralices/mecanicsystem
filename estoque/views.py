from django.shortcuts import render, redirect
from .models import Peca

def listar_pecas(request):
    pecas = Peca.objects.all()
    return render(request, 'estoque/listar.html', {'pecas': pecas})

def adicionar_peca(request):
    if request.method == 'POST':
        Peca.objects.create(
            nome=request.POST['nome'],
            quantidade=request.POST['quantidade'],
            preco_custo=request.POST['preco_custo'].replace(',', '.'),
            preco_venda=request.POST['preco_venda'].replace(',', '.'),
            fornecedor=request.POST['fornecedor']
        )
        return redirect('listar_pecas')
    return render(request, 'estoque/adicionar.html')
