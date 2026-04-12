from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_pecas, name='listar_pecas'),
    path('adicionar/', views.adicionar_peca, name='adicionar_peca'),
]
