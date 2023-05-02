from unicodedata import name
from django.urls import path
from . import views
from .views import LoginView
from .views import CadastroInstituicaoView
from .views import CadastroUsuarioView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('cadastro-instituicao', CadastroInstituicaoView.as_view(), name='cadastro-instituicao'),
    path('cadastro-usuario', CadastroUsuarioView.as_view(), name='cadastro-usuario'),
    path('home', views.home, name='home')
]
