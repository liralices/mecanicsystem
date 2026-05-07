from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
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


def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        cliente.nome = request.POST['nome']
        cliente.telefone = request.POST['telefone']
        cliente.email = request.POST['email']
        cliente.save()

        return redirect('listar_clientes')

    return render(request, 'clientes/editar.html', {'cliente': cliente})


def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')

    return render(
        request,
        'clientes/confirmar_exclusao.html',
        {'cliente': cliente}
    )


def detalhe_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    veiculos = cliente.veiculos.all()

    return render(
        request,
        'clientes/detalhe.html',
        {
            'cliente': cliente,
            'veiculos': veiculos
        }
    )


def listar_veiculos(request, cliente_id=None):

    if cliente_id:
        cliente = get_object_or_404(Cliente, id=cliente_id)
        veiculos = cliente.veiculos.all()

        return render(
            request,
            'clientes/veiculos_listar.html',
            {
                'veiculos': veiculos,
                'cliente': cliente
            }
        )

    veiculos = Veiculo.objects.all()

    return render(
        request,
        'clientes/veiculos_listar.html',
        {'veiculos': veiculos}
    )


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
            quilometragem=int(
                request.POST.get('quilometragem', 0)
            )
        )

        return redirect(
            'detalhe_cliente',
            id=cliente.id
        )

    return render(
        request,
        'clientes/veiculos_adicionar.html',
        {'cliente': cliente}
    )


def editar_veiculo(request, id):

    veiculo = get_object_or_404(Veiculo, id=id)

    if request.method == 'POST':

        veiculo.placa = request.POST['placa'].upper()
        veiculo.marca = request.POST['marca']
        veiculo.modelo = request.POST['modelo']
        veiculo.ano = int(request.POST['ano'])
        veiculo.cor = request.POST.get('cor', '')
        veiculo.quilometragem = int(
            request.POST.get('quilometragem', 0)
        )

        veiculo.save()

        return redirect(
            'detalhe_cliente',
            id=veiculo.cliente.id
        )

    return render(
        request,
        'clientes/veiculos_editar.html',
        {'veiculo': veiculo}
    )


def excluir_veiculo(request, id):

    veiculo = get_object_or_404(Veiculo, id=id)
    cliente_id = veiculo.cliente.id

    if request.method == 'POST':
        veiculo.delete()

        return redirect(
            'detalhe_cliente',
            id=cliente_id
        )

    return render(
        request,
        'clientes/veiculos_confirmar_exclusao.html',
        {'veiculo': veiculo}
    )


# FUNÇÃO JSON PARA AJAX/API
def veiculos_json(request, cliente_id):

    cliente = get_object_or_404(Cliente, id=cliente_id)
    veiculos = cliente.veiculos.all()

    dados = [
        {
            'id': veiculo.id,
            'placa': veiculo.placa,
            'marca': veiculo.marca,
            'modelo': veiculo.modelo,
            'ano': veiculo.ano,
            'cor': veiculo.cor,
            'quilometragem': veiculo.quilometragem,
        }
        for veiculo in veiculos
    ]

    return JsonResponse(dados, safe=False)


# Endpoint para retornar informações de um veículo específico
def veiculo_info(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    
    dados = {
        'id': veiculo.id,
        'placa': veiculo.placa,
        'marca': veiculo.marca,
        'modelo': veiculo.modelo,
        'ano': veiculo.ano,
        'cor': veiculo.cor,
        'quilometragem': veiculo.quilometragem,
    }

    return JsonResponse(dados)


# Endpoint para criar novo veículo via AJAX
def criar_veiculo(request):
    if request.method == 'POST':
        try:
            cliente_id = request.POST.get('cliente')
            cliente = get_object_or_404(Cliente, id=cliente_id)
            
            veiculo = Veiculo.objects.create(
                cliente=cliente,
                placa=request.POST.get('placa', '').upper(),
                marca=request.POST.get('marca', ''),
                modelo=request.POST.get('modelo', ''),
                ano=int(request.POST.get('ano', 0)),
                cor=request.POST.get('cor', ''),
                quilometragem=int(request.POST.get('quilometragem', 0))
            )
            
            return JsonResponse({
                'success': True,
                'veiculo_id': veiculo.id,
                'message': 'Veículo criado com sucesso!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})
