from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_pecas, name='listar_pecas'),
    path('adicionar/', views.adicionar_peca, name='adicionar_peca'),
    path('editar/<int:id>/', views.editar_peca, name='editar_peca'),
    path('excluir/<int:id>/', views.excluir_peca, name='excluir_peca'),
]


