from django.urls import path
from .views import ListaContato, DeletarUsuario, EditarUsuario, LoginView, LogoutView, CadastroInstituicaoView, CadastroUsuarioView, InstituicoesView, HomeUsuarios, HomeInstituicao, CardMapView, Index, DetalhesInstituicao, DetalhesUsuario, MenuUsuario, ContatoView, SobreView
urlpatterns = [
    path('index', Index.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('cadastro-instituicao', CadastroInstituicaoView.as_view(), name='cadastro-instituicao'),
    path('cadastro-usuario', CadastroUsuarioView.as_view(), name='cadastro-usuario'),
    path('instituicoes', InstituicoesView.as_view(), name='instituicoes'),
    path('home-usuario', HomeUsuarios.as_view(), name='home-usuario'),
    path('home-instituicao', HomeInstituicao.as_view(), name='home-instituicao'),
    path('card-map', CardMapView.as_view(), name='card-map'),
    path('detalhe-instituicao', DetalhesInstituicao.as_view(), name='detalhe-instituicao'),
    path('detalhe-usuario', DetalhesUsuario.as_view(), name='detalhe-usuario'),
    path('deletar-usuario', DeletarUsuario.as_view(), name='deletar-usuario'),
    path('menu-usuario', MenuUsuario.as_view(), name='menu-usuario'),
    path('editar-usuario', EditarUsuario.as_view(), name='editar-usuario'),
    path('contato', ContatoView.as_view(), name='contato'),
    path('sobre', SobreView.as_view(), name='sobre'),
    path('contatos', ListaContato.as_view(), name='lista_contatos'),
]
