from django.shortcuts import render, redirect
from .models import Cliente

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/listar.html', {'clientes': clientes})

def adicionar_cliente(request):
    if request.method == 'POST':
        Cliente.objects.create(
            nome=request.POST['nome'],
            telefone=request.POST['telefone'],
            email=request.POST['email']
        )
        return redirect('listar_clientes')
    return render(request, 'clientes/adicionar.html')

def excluir_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'clientes/confirmar_exclusao.html', {'cliente': cliente})