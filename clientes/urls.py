from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_clientes, name='listar_clientes'),
    path('adicionar/', views.adicionar_cliente, name='adicionar_cliente'),
    path('excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),
]

