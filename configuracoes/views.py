from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import ConfiguracaoOficina

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
