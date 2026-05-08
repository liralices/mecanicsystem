from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_clientes, name='listar_clientes'),
    path('adicionar/', views.adicionar_cliente, name='adicionar_cliente'),
    path('editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),
    path('detalhe/<int:id>/', views.detalhe_cliente, name='detalhe_cliente'),
    path('veiculos/', views.listar_veiculos, name='listar_veiculos'),
    path('detalhe/<int:cliente_id>/veiculos/', views.listar_veiculos, name='listar_veiculos_cliente'),
    path('detalhe/<int:cliente_id>/veiculo/adicionar/', views.adicionar_veiculo, name='adicionar_veiculo'),
    path('veiculo/editar/<int:id>/', views.editar_veiculo, name='editar_veiculo'),
    path('veiculo/excluir/<int:id>/', views.excluir_veiculo, name='excluir_veiculo'),
    path('veiculos-json/<int:cliente_id>/', views.veiculos_json, name='veiculos_json'),
    path('veiculo-info/<int:veiculo_id>/', views.veiculo_info, name='veiculo_info'),
    path('criar-veiculo/', views.criar_veiculo, name='criar_veiculo'),
    path('criar-cliente/', views.criar_cliente, name='criar_cliente'),
]



