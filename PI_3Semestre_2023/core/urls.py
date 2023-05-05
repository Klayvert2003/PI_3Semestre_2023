from unicodedata import name
from django.urls import path
from . import views
from .views import LoginView, CadastroInstituicaoView, CadastroUsuarioView, InstituicoesView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('cadastro-instituicao', CadastroInstituicaoView.as_view(), name='cadastro-instituicao'),
    path('cadastro-usuario', CadastroUsuarioView.as_view(), name='cadastro-usuario'),
    path('instituicoes', InstituicoesView.as_view(), name='instituicoes'),
    path('home', views.home, name='home')
]
