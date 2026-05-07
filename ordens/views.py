from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
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
    erro = None

    if request.method == 'POST':
        # Verifica estoque antes de criar
        for peca in pecas:
            qtd = request.POST.get(f'peca_{peca.id}')
            if qtd and int(qtd) > 0:
                if int(qtd) > peca.quantidade:
                    erro = f'Estoque insuficiente para "{peca.nome}". Disponível: {peca.quantidade} un.'
                    break

        if not erro:
            cliente = Cliente.objects.get(id=request.POST['cliente'])
            veiculo_id = request.POST.get('veiculo')
            veiculo = Veiculo.objects.get(id=veiculo_id) if veiculo_id else None
            mao_de_obra = Decimal(request.POST['mao_de_obra'].replace(',', '.'))
            
            # Se marcou "concluida", seta o status como concluida, senão usa o status padrão
            if request.POST.get('concluida') == 'on':
                status = 'concluida'
            else:
                status = request.POST.get('status', 'aberta')

            ordem = OrdemServico.objects.create(
                cliente=cliente,
                veiculo=veiculo,
                descricao=request.POST['descricao'],
                mao_de_obra=mao_de_obra,
                status=status
            )

            for peca in pecas:
                qtd = request.POST.get(f'peca_{peca.id}')
                if qtd and int(qtd) > 0:
                    quantidade = int(qtd)
                    ItemOS.objects.create(
                        ordem_servico=ordem,
                        peca=peca,
                        quantidade=quantidade
                    )
                    # Baixa automática no estoque
                    peca.quantidade -= quantidade
                    peca.save()

            ordem.calcular_total()
            return redirect('listar_ordens')

    return render(request, 'ordens/adicionar.html', {
        'clientes': clientes,
        'pecas': pecas,
        'veiculos': veiculos,
        'erro': erro
    })

def editar_ordem(request, id):
    ordem = get_object_or_404(OrdemServico, id=id)
    clientes = Cliente.objects.all()
    veiculos = Veiculo.objects.all()

    if request.method == 'POST':
        ordem.cliente = Cliente.objects.get(id=request.POST['cliente'])
        veiculo_id = request.POST.get('veiculo')
        ordem.veiculo = Veiculo.objects.get(id=veiculo_id) if veiculo_id else None
        ordem.descricao = request.POST['descricao']
        ordem.mao_de_obra = Decimal(request.POST['mao_de_obra'].replace(',', '.'))
        
        # Se marcou "concluida", seta o status como concluida, senão usa o status padrão
        if request.POST.get('concluida') == 'on':
            ordem.status = 'concluida'
        else:
            ordem.status = request.POST.get('status', 'aberta')
        
        ordem.save()
        ordem.calcular_total()
        return redirect('listar_ordens')

    return render(request, 'ordens/editar.html', {
        'ordem': ordem,
        'clientes': clientes,
        'veiculos': veiculos
    })

def excluir_ordem(request, id):
    ordem = get_object_or_404(OrdemServico, id=id)
    if request.method == 'POST':
        # Devolve as peças ao estoque ao excluir a OS
        for item in ordem.itemos_set.all():
            item.peca.quantidade += item.quantidade
            item.peca.save()
        ordem.delete()
        return redirect('listar_ordens')
    return render(request, 'ordens/confirmar_exclusao.html', {'ordem': ordem})


def toggle_concluida(request, id):
    if request.method == 'POST':
        ordem = get_object_or_404(OrdemServico, id=id)
        # Alterna o status entre "concluida" e "aberta"
        ordem.status = 'aberta' if ordem.status == 'concluida' else 'concluida'
        ordem.save()
        return JsonResponse({'status': ordem.status})
    return JsonResponse({'error': 'Método não permitido'}, status=405)


