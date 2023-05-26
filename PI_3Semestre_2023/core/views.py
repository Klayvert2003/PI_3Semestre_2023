from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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
                return HttpResponse('CNPJ Inválido!!!')

        email = request.POST.get('email')
        usuario = request.POST.get('usuario')
        password = request.POST.get('senha')
        
        #dados = DadosInstituicao.objects.create(nome_instituicao=nome_instituicao, cep=infos[0], num=infos[1], cnpj=cnpj, 
        #rua=address[0], bairro=address[1], cidade=address[2], 
        #estado=address[3], latitude=address[4], longitude=address[5])
        
        #user = User.objects.filter(email=email).first()
        #if user:
        #    return HttpResponse('Já existe um usuário com este email!!!')

        #user = User.objects.create_user(username=usuario, email=email, password=password)
        
        data = {
            'usuario': usuario,
            'senha': password,
            'email': email,
            'nome_instituicao': nome_instituicao,
            'cep': infos[0],
            'num': infos[1],
            'cnpj': cnpj,
            'rua': address[0],
            'bairro': address[1],
            'cidade': address[2],
            'estado': address[3],
            'latitude': address[4],
            'longitude': address[5],
        }
        
        #if data:
        return render(request, 'detalhes-instituicao.html', {'dados': data})

        #return redirect('instituicoes')

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
                return HttpResponse('Insira apenas números!!!')

        email = request.POST.get('email')
        usuario = request.POST.get('usuario')
        password = request.POST.get('senha')
        confirm_password = request.POST.get('confirma-senha')
        if password != confirm_password:
            return HttpResponse('Senhas divergentes, digite a senha idêntica a inserida anteriormente')

        dados = DadosUsuarios.objects.create(nome_usuario=nome_completo, cep=cep, num=num,
        rua=address[0], bairro=address[1], cidade=address[2], 
        estado=address[3])
        
        user = User.objects.filter(email=email).first()
        if user:
            return HttpResponse('Já existe um usuário com este email!!!')
        
        user = User.objects.create_user(username=usuario, email=email, password=password)

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

            return render(request, 'home-usuario.html')
        else:
            return HttpResponse('Email ou senha inválidos')
        
class InstituicoesView(GoogleMapsAPI, View):
    def get(self, request):
        dados = list(DadosInstituicao.objects.all().values('id', 'nome_instituicao', 'latitude', 'longitude'))

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
    
class DetalhesInstituicao(View):
    def get(self, request):
        template_name = 'detalhes-instituicao.html'
        return render(request, template_name)
    
    def post(self, request):
        usuario = request.POST.get('usuario')
        password = request.POST.get('senha')
        nome_instituicao = request.POST.get('nome-instituicao')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        num = request.POST.get('num')
        bairro = request.POST.get('cidade')
        cidade = request.POST.get('nome-instituicao')
        complemento = request.POST.get('complemento')
        estado = request.POST.get('estado')
        tel = request.POST.get('telefone')
        cel = request.POST.get('celular')
        email = request.POST.get('email')
        cnpj = request.POST.get('cnpj')
        descricao = request.POST.get('descreva')
        forma_ajuda1 = request.POST.get('doacao1')
        forma_ajuda2 = request.POST.get('doacao2')
        forma_ajuda3 = request.POST.get('doacao3')
        
        DadosInstituicao.objects.create(nome_instituicao=nome_instituicao, cep=cep, num=num, cnpj=cnpj, 
        rua=rua, bairro=bairro, cidade=cidade, 
        estado=estado, )
        #latitude=address[4], longitude=address[5])
        
        user = User.objects.filter(email=email).first()
        if user:
            return HttpResponse('Já existe um usuário com este email!!!')

        #user = User.objects.create_user(username=usuario, email=email, password=password)
        #user = User.objects.update(username=usuario, email=email, password=password)
    
class InfoUsuario(TemplateView):
    def get(self, request):
        dados = list(DadosUsuarios.objects.all())
        template_name = 'Informacoes_de_usuario.html'
        return render(request, template_name, {'dados': dados})