from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import OrdemServico, ItemOS
from clientes.models import Cliente, Veiculo
from estoque.models import Peca
from configuracoes.models import Funcionario
from decimal import Decimal
import re

def converter_valor_monetario(valor_str):
    """Converte valor monetário brasileiro (1.234,56) para Decimal"""
    # Remove pontos (separadores de milhares) e troca vírgula por ponto
    valor_limpo = re.sub(r'\.', '', valor_str).replace(',', '.')
    return Decimal(valor_limpo)

def listar_ordens(request):
    ordens = OrdemServico.objects.order_by('-valor_total')
    return render(request, 'ordens/listar.html', {'ordens': ordens})

def adicionar_ordem(request):
    clientes = Cliente.objects.all()
    pecas = Peca.objects.all().order_by('nome')
    veiculos = Veiculo.objects.all()
    funcionarios = Funcionario.objects.all()
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
            funcionario_id = request.POST.get('funcionario')
            funcionario = Funcionario.objects.get(id=funcionario_id) if funcionario_id else None
            mao_de_obra = converter_valor_monetario(request.POST['mao_de_obra'])
            
            status = request.POST.get('status', 'aberta')

            ordem = OrdemServico.objects.create(
                cliente=cliente,
                veiculo=veiculo,
                funcionario=funcionario,
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
        'funcionarios': funcionarios,
        'erro': erro
    })

def editar_ordem(request, id):
    ordem = get_object_or_404(OrdemServico, id=id)
    clientes = Cliente.objects.all()
    veiculos = Veiculo.objects.all()
    funcionarios = Funcionario.objects.all()

    if request.method == 'POST':
        ordem.cliente = Cliente.objects.get(id=request.POST['cliente'])
        veiculo_id = request.POST.get('veiculo')
        ordem.veiculo = Veiculo.objects.get(id=veiculo_id) if veiculo_id else None
        funcionario_id = request.POST.get('funcionario')
        ordem.funcionario = Funcionario.objects.get(id=funcionario_id) if funcionario_id else None
        ordem.descricao = request.POST['descricao']
        ordem.mao_de_obra = converter_valor_monetario(request.POST['mao_de_obra'])
        
        ordem.status = request.POST.get('status', 'aberta')
        
        ordem.save()
        ordem.calcular_total()
        return redirect('listar_ordens')

    return render(request, 'ordens/editar.html', {
        'ordem': ordem,
        'clientes': clientes,
        'veiculos': veiculos,
        'funcionarios': funcionarios
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


