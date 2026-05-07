from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Veiculo

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

def listar_veiculos(request, cliente_id=None):
    if cliente_id:
        cliente = get_object_or_404(Cliente, id=cliente_id)
        veiculos = cliente.veiculos.all()
        return render(request, 'clientes/veiculos_listar.html', {'veiculos': veiculos, 'cliente': cliente})
    veiculos = Veiculo.objects.all()
    return render(request, 'clientes/veiculos_listar.html', {'veiculos': veiculos})

def adicionar_veiculo(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        Veiculo.objects.create(
            cliente=cliente,
            placa=request.POST['placa'].upper(),
            marca=request.POST['marca'],
            modelo=request.POST['modelo'],
            ano=int(request.POST['ano']),
            cor=request.POST.get('cor', ''),
            quilometragem=int(request.POST.get('quilometragem', 0))
        )
        return redirect('listar_veiculos_cliente', cliente_id=cliente.id)
    return render(request, 'clientes/veiculos_adicionar.html', {'cliente': cliente})

def editar_veiculo(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    if request.method == 'POST':
        veiculo.placa = request.POST['placa'].upper()
        veiculo.marca = request.POST['marca']
        veiculo.modelo = request.POST['modelo']
        veiculo.ano = int(request.POST['ano'])
        veiculo.cor = request.POST.get('cor', '')
        veiculo.quilometragem = int(request.POST.get('quilometragem', 0))
        veiculo.save()
        return redirect('listar_veiculos_cliente', cliente_id=veiculo.cliente.id)
    return render(request, 'clientes/veiculos_editar.html', {'veiculo': veiculo})

def excluir_veiculo(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    cliente_id = veiculo.cliente.id
    if request.method == 'POST':
        veiculo.delete()
        return redirect('listar_veiculos_cliente', cliente_id=cliente_id)
    return render(request, 'clientes/veiculos_confirmar_exclusao.html', {'veiculo': veiculo})