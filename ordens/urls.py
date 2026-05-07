from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_ordens, name='listar_ordens'),
    path('adicionar/', views.adicionar_ordem, name='adicionar_ordem'),
    path('editar/<int:id>/', views.editar_ordem, name='editar_ordem'),
    path('excluir/<int:id>/', views.excluir_ordem, name='excluir_ordem'),
]



