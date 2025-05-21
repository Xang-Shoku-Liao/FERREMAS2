from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),  # <-- Cambia aquí
    path('pagar/', views.pagar, name='pagar'),
    path('retorno/', views.retorno, name='retorno'),
    path('api_productos/', views.api_productos, name='api_productos'),
]
