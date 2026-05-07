from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_clientes, name='listar_clientes'),
    path('adicionar/', views.adicionar_cliente, name='adicionar_cliente'),
    path('excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),
    path('<int:cliente_id>/veiculos/', views.listar_veiculos, name='listar_veiculos_cliente'),
    path('<int:cliente_id>/veiculos/adicionar/', views.adicionar_veiculo, name='adicionar_veiculo'),
    path('veiculo/<int:id>/editar/', views.editar_veiculo, name='editar_veiculo'),
    path('veiculo/<int:id>/excluir/', views.excluir_veiculo, name='excluir_veiculo'),
]

