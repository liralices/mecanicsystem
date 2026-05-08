from django.urls import path
from . import views

urlpatterns = [
    path('editar/', views.editar_configuracoes, name='editar_configuracoes'),
    path('funcionarios/', views.listar_funcionarios, name='listar_funcionarios'),
    path('funcionarios/adicionar/', views.adicionar_funcionario, name='adicionar_funcionario'),
    path('funcionarios/editar/<int:id>/', views.editar_funcionario, name='editar_funcionario'),
    path('funcionarios/excluir/<int:id>/', views.excluir_funcionario, name='excluir_funcionario'),
    path('criar-funcionario/', views.criar_funcionario, name='criar_funcionario'),
]
