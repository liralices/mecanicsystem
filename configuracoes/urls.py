from django.urls import path
from . import views

urlpatterns = [
    path('editar/', views.editar_configuracoes, name='editar_configuracoes'),
]
