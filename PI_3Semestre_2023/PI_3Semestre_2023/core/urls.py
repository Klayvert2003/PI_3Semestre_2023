from django.urls import path
from .views import IndexView, LoginView, CadastroInstituicaoView, CadastroUsuarioView, InstituicoesView, HomeUsuarios, CardMapView

urlpatterns = [
    path('index', IndexView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('cadastro-instituicao', CadastroInstituicaoView.as_view(), name='cadastro-instituicao'),
    path('cadastro-usuario', CadastroUsuarioView.as_view(), name='cadastro-usuario'),
    path('instituicoes', InstituicoesView.as_view(), name='instituicoes'),
    path('home-usuario', HomeUsuarios.as_view(), name='home-usuario'),
    path('card-map', CardMapView.as_view(), name='card-map'),
]
