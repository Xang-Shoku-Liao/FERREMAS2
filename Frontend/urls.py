from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('productos/', views.lista_productos, name='productos'),
    path('contacto/', views.contacto, name='contacto'),
    path('registro/', views.registro, name='registro'),
    path('retorno/', views.retorno, name='retorno'),  # Usa tu vista de retorno
    path('pagar/', views.pagar, name='pagar'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('api_productos/', views.api_productos, name='api_productos'),  # Tu API
]
