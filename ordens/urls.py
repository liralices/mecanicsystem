from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_ordens, name='listar_ordens'),
    path('adicionar/', views.adicionar_ordem, name='adicionar_ordem'),
]

