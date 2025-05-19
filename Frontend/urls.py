from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pagar/', views.pagar, name='pagar'),
    path('retorno/', views.retorno, name='retorno'),
]
