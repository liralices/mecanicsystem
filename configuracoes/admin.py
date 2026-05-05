from django.contrib import admin
from .models import ConfiguracaoOficina

@admin.register(ConfiguracaoOficina)
class ConfiguracaoOficinaAdmin(admin.ModelAdmin):
    list_display = ('nome_oficina', 'email', 'data_atualizacao')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome_oficina', 'logo')
        }),
        ('Contato', {
            'fields': ('telefone', 'email', 'endereco')
        }),
    )
