from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# My functions
from core.models import DadosInstituicao, DadosUsuarios
from api.ValidaCNPJ import ValidaCNPJ
from api.GoogleMapsAPI import GoogleMapsAPI
from PI_3Semestre_2023.settings import API_KEY

class Index(View):
    def get(self, request):
        return render(request, 'index.html')
    
    def post(self, request):
        ...

class CadastroInstituicaoView(ValidaCNPJ, GoogleMapsAPI, View):
    def get(self, request):
        return render(request, 'cadastro-instituicao.html')
        
    def post(self, request): 
        nome_instituicao = request.POST.get('nome-completo')
        cnpj = request.POST.get('cnpj')
        if cnpj:
            try:
                cnpj = str(cnpj).replace('.', '').replace('-', '').replace('/', '')
                infos = self.BuscaCNPJ(cnpj=cnpj)
                address = self.get_complete_address(cep=infos[0], num=infos[1])
            except AttributeError:
                messages.error(request, 'CNPJ Inválido!!!')
                return redirect('cadastro-instituicao')

        email = request.POST.get('email')
        usuario = request.POST.get('usuario')
        password = request.POST.get('senha')
        
        data = {
            'usuario': usuario,
            'senha': password,
            'email': email,
            'nome_instituicao': nome_instituicao,
            'cep': infos[0],
            'num': infos[1],
            'complemento': infos[2],
            'telefone': infos[3],
            'cnpj': cnpj,
            'rua': address[0],
            'bairro': address[1],
            'cidade': address[2],
            'estado': address[3],
            'latitude': address[4],
            'longitude': address[5],
        }

        request.session['email'] = email
        request.session['usuario'] = usuario
        request.session['senha'] = password
        return render(request, 'detalhes-instituicao.html', {'dados': data})

class CadastroUsuarioView(GoogleMapsAPI, View):
    def get(self, request):
        return render(request, 'cadastro-usuario.html')
    
    def post(self, request):
        nome_completo = request.POST.get('nome-completo')     
        cep = request.POST.get('cep')
        num = request.POST.get('num')
        if cep and num:
            try:
                cep = str(cep).replace('-', '').replace('.', '')
                num = str(num)
                address = GoogleMapsAPI().get_complete_address(cep=cep, num=num)
            except IndexError:
                messages.error(request, 'Insira apenas números!!!')
                return redirect('cadastro-usuario')

        email = request.POST.get('email')
        usuario = request.POST.get('usuario')
        password = request.POST.get('senha')

        user = User.objects.filter(email=email).first()
        if user:
            messages.error(request, 'Já existe um usuário com este email!!!')
            return redirect('cadastro-usuario')
        
        user = User.objects.create_user(username=usuario, email=email, password=password)

        DadosUsuarios.objects.create(id=user.id, nome_usuario=nome_completo, cep=cep, num=num,
        rua=address[0], bairro=address[1], cidade=address[2], 
        estado=address[3])

        return redirect("instituicoes")

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
        
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            user_id = user.id
            request.session['user_id'] = user_id
            return render(request, 'home-usuario.html', {'user_id': user_id})
        else:
            messages.error(request, 'Email ou senha inválidos!!!')
            return render(request, 'login.html')
        
class LogoutView(TemplateView):
    def get(self, request):
        messages.success(request, 'Realizando logout!!!')
        logout(request)
        return redirect('index')
        
class InstituicoesView(GoogleMapsAPI, View):
    def get(self, request):
        dados = list(DadosInstituicao.objects.all().values('id', 'nome_instituicao', 'latitude', 'longitude', 'descricao'))

        return render(request, 'instituicoes.html', {'dados': dados})

    def post(self):
        return redirect('card-map')

class CardMapView(View):
    def get(self, request):
        lat = request.GET.get('latitude', None)
        lon = request.GET.get('longitude', None)

        if lat and lon:
            contexto = {
                'latitude': lat,
                'longitude': lon,
                'API_KEY': API_KEY
            }
            return render(request, 'card-map.html', contexto)
        else:
            return redirect('instituicoes')

class HomeUsuarios(TemplateView):
    # @login_required(login_url='/auth/login')
    def get(self, request):
        # if request.user.is_authenticated:
        template_name = 'home-usuario.html'
        return render(request, template_name)
        
    def post(self, request):
        return render(request, 'instituicoes.html')

class HomeInstituicao(TemplateView):
    def get(self, request):
        template_name='lp_instituicao.html'
        return render(request, template_name)
    
class DetalhesInstituicao(GoogleMapsAPI, ValidaCNPJ, View):
    def get(self, request):
        template_name = 'detalhes-instituicao.html'
        return render(request, template_name)
    
    def post(self, request):
        email = request.session.get('email')
        usuario = request.session.get('usuario')
        senha = request.session.get('senha')
        print(email, usuario, senha)
        nome_instituicao = request.POST.get('nome-instituicao')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        num = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        complemento = request.POST.get('complemento')
        estado = request.POST.get('estado')
        tel = request.POST.get('telefone')
        cel = request.POST.get('celular')
        cnpj = request.POST.get('cnpj')
        if cnpj:
            try:
                cnpj = str(cnpj).replace('.', '').replace('-', '').replace('/', '')
                infos = self.BuscaCNPJ(cnpj=cnpj)
                address = self.get_complete_address(cep=infos[0], num=infos[1])
            except AttributeError:
                messages.error(request, 'CNPJ Inválido!!!')
                return redirect('detalhes-instituicao')
        descricao = request.POST.get('descreva')
        forma_ajuda1 = request.POST.get('doacao1')
        forma_ajuda2 = request.POST.get('doacao2')
        forma_ajuda3 = request.POST.get('doacao3')
        user = User.objects.filter(email=email).first()
        if user:
            messages.error(request, 'Já existe um usuário com este email!!!')
            return redirect('detalhes-instituicao')

        user = User.objects.create_user(username=usuario, email=email, password=senha)
        
        DadosInstituicao.objects.create(id=user.id, email=email, senha=senha, cel=cel, tel=tel, descricao=descricao, forma_ajuda1=forma_ajuda1, 
        forma_ajuda2=forma_ajuda2, forma_ajuda3=forma_ajuda3, nome_instituicao=nome_instituicao, 
        cep=cep, num=num, cnpj=cnpj, rua=rua, complemento=complemento, bairro=bairro, cidade=cidade, 
        estado=estado, latitude=address[4], longitude=address[5])
        
        return redirect('instituicoes')
    
class InfoUsuario(TemplateView):
    def get(self, request):
        dados = list(DadosUsuarios.objects.all())
        template_name = 'Informacoes_de_usuario.html'
        return render(request, template_name, {'dados': dados})
    
class DeletarUsuario(View):
    @staticmethod
    def get(request):
        id_usuario = request.session.get('user_id')
        auth_user = User.objects.get(id=id_usuario)
        usuario = None
        try:
            try:
                usuario = DadosUsuarios.objects.get(id=id_usuario)
                usuario.delete()
                print(f'Usuário de id {id_usuario} deletado')
            except DadosUsuarios.DoesNotExist:
                print("Usuário não é doador/voluntário.")
                pass
            try:
                usuario = DadosInstituicao.objects.get(id=id_usuario)
                usuario.delete()
                print(f'Usuário de id {id_usuario} deletado')
            except DadosInstituicao.DoesNotExist:
                print("Usuário não é uma instituição.")
                pass
        finally:
            if auth_user is not None:
                auth_user.delete()

        return redirect('index')
    
class MenuUsuario(TemplateView):
    def get(self, request):
        template_name='menu-usuario.html'
        return render(request, template_name)        