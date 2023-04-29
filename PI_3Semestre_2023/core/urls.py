from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('cadastro-instituicao', views.cadastro_instituicao, name='cadastro-instituicao'),
    path('cadastro-usuario', views.cadastro_usuario, name='cadastro-usuario'),
    path('cep', views.cep, name='cep'),
    path('maps', views.MapsAPI, name='maps'),
    path('home', views.home, name='home')
]
