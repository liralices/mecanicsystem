from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import ConfiguracaoOficina, Funcionario

def editar_configuracoes(request):
    try:
        config = ConfiguracaoOficina.objects.first()
        if not config:
            config = ConfiguracaoOficina.objects.create()
    except ConfiguracaoOficina.DoesNotExist:
        config = ConfiguracaoOficina.objects.create()
    
    if request.method == 'POST':
        config.nome_oficina = request.POST.get('nome_oficina', config.nome_oficina)
        config.telefone = request.POST.get('telefone', '')
        config.email = request.POST.get('email', '')
        config.endereco = request.POST.get('endereco', '')
        
        if 'logo' in request.FILES:
            config.logo = request.FILES['logo']
        
        config.save()
        return redirect('/')
    
    return render(request, 'configuracoes/editar.html', {'config': config})

def get_configuracao():
    try:
        return ConfiguracaoOficina.objects.first() or ConfiguracaoOficina.objects.create()
    except:
        return None

# Views para Funcionários
def listar_funcionarios(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'configuracoes/funcionarios_listar.html', {'funcionarios': funcionarios})

def adicionar_funcionario(request):
    if request.method == 'POST':
        Funcionario.objects.create(
            nome=request.POST['nome'],
            telefone=request.POST.get('telefone', ''),
            email=request.POST.get('email', '')
        )
        return redirect('listar_funcionarios')
    
    return render(request, 'configuracoes/funcionarios_adicionar.html')

def editar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    
    if request.method == 'POST':
        funcionario.nome = request.POST['nome']
        funcionario.telefone = request.POST.get('telefone', '')
        funcionario.email = request.POST.get('email', '')
        funcionario.save()
        return redirect('listar_funcionarios')
    
    return render(request, 'configuracoes/funcionarios_editar.html', {'funcionario': funcionario})

def excluir_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    
    if request.method == 'POST':
        funcionario.delete()
        return redirect('listar_funcionarios')
    
    return render(request, 'configuracoes/funcionarios_confirmar_exclusao.html', {'funcionario': funcionario})

# Endpoint para criar novo funcionário via AJAX
def criar_funcionario(request):
    from django.http import JsonResponse
    if request.method == 'POST':
        try:
            funcionario = Funcionario.objects.create(
                nome=request.POST.get('nome', ''),
                telefone=request.POST.get('telefone', ''),
                email=request.POST.get('email', '')
            )
            
            return JsonResponse({
                'success': True,
                'funcionario_id': funcionario.id,
                'message': 'Funcionário criado com sucesso!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})
