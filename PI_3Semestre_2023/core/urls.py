from django.urls import path
from .views import LoginView, CadastroInstituicaoView, CadastroUsuarioView, InstituicoesView, HomeUsuarios, HomeInstituicao, CardMapView, Index, InfoInstituicao, InfoUsuario

urlpatterns = [
    path('index', Index.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('cadastro-instituicao', CadastroInstituicaoView.as_view(), name='cadastro-instituicao'),
    path('cadastro-usuario', CadastroUsuarioView.as_view(), name='cadastro-usuario'),
    path('instituicoes', InstituicoesView.as_view(), name='instituicoes'),
    path('home-usuario', HomeUsuarios.as_view(), name='home-usuario'),
    path('home-instituicao', HomeInstituicao.as_view(), name='home-instituicao'),
    path('card-map', CardMapView.as_view(), name='card-map'),
    path('info-instituicao', InfoInstituicao.as_view(), name='info-instituicao'),
    path('info-usuario', InfoUsuario.as_view(), name='info-usuario'),
]
