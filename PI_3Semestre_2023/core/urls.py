from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('cep', views.cep, name='cep'),
    path('maps', views.testeMapsAPI, name='maps'),
    path('home', views.home, name='home')
]