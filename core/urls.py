from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('clientes/', include('clientes.urls')),
    path('estoque/', include('estoque.urls')),
    path('ordens/', include('ordens.urls')),
]


