from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
# My functions
from core.models import DadosInstituicao, DadosUsuarios
from api.correiosAPI import BuscaCEP
from api.GoogleMapsAPI import GoogleMapsAPI

def get_address(cep):
    address = GoogleMapsAPI
    data = address.buscar_endereco(address=cep)
    rua = str(data[0]['formatted_address']).split('-')[0].strip()
    bairro = str(data[0]['formatted_address']).split('-')[1].split(',')[0].strip()
    cidade = str(data[0]['formatted_address']).split('-')[1].split(',')[1].strip()
    estado = str(data[0]['formatted_address']).split('-')[2].split(',')[0].strip()

    return rua, bairro, cidade, estado

def get_cnpj(cnpj):
    ...

def cadastro_instituicao(request):
    if request.method == 'GET':
        return render(request, 'cadastro-instituicao.html')
    else:   
        nome_instituicao = request.POST.get('nome-completo')     
        cep = request.POST.get('cep')
        if cep:
            try:
                cep = str(cep).replace('-', '').replace('.', '')
                get_address(cep=cep)
            except IndexError:
                return HttpResponse('Insira apenas números!!!')
            
        cnpj = request.POST.get('cnpj')
        if cnpj:
            try:
                cep = str(cnpj).replace('-', '').replace('.', '')
                get_cnpj(cep=cep)
            except IndexError:
                return HttpResponse('Insira apenas números!!!')

        email = request.POST.get('email')
        usuario = request.POST.get('usuario')
        password = request.POST.get('senha')
        confirm_password = request.POST.get('confirma-senha')
        if password != confirm_password:
            return HttpResponse('Senhas divergentes, digite a senha idêntica a inserida anteriormente')

        dados = DadosInstituicao.objects.create(nome_instituicao=nome_instituicao, cep=cep, cnpj=cnpj, 
        rua=get_address(cep=cep)[0], bairro=get_address(cep=cep)[1], cidade=get_address(cep=cep)[2], 
        estado=get_address(cep=cep)[3])
        
        user = User.objects.filter(email=email).first()
        if user:
            return HttpResponse('Já existe um usuário com este email!!!')
        
        user = User.objects.create_user(username=usuario, email=email, password=password)

        return HttpResponse("Usuário cadastrado!")

def cadastro_usuario(request):
    if request.method == 'GET':
        return render(request, 'cadastro-usuario.html')
    else:
        nome_completo = request.POST.get('nome-completo')     
        cep = request.POST.get('cep')
        if cep:
            try:
                cep = str(cep).replace('-', '').replace('.', '')
                get_address(cep=cep)
            except IndexError:
                return HttpResponse('Insira apenas números!!!')

        email = request.POST.get('email')
        usuario = request.POST.get('usuario')
        password = request.POST.get('senha')
        confirm_password = request.POST.get('confirma-senha')
        if password != confirm_password:
            return HttpResponse('Senhas divergentes, digite a senha idêntica a inserida anteriormente')

        dados = DadosUsuarios.objects.create(nome_usuario=nome_completo, cep=cep, 
        rua=get_address(cep=cep)[0], bairro=get_address(cep=cep)[1], cidade=get_address(cep=cep)[2], 
        estado=get_address(cep=cep)[3])
        
        user = User.objects.filter(email=email).first()
        if user:
            return HttpResponse('Já existe um usuário com este email!!!')
        
        user = User.objects.create_user(username=usuario, email=email, password=password)

        return HttpResponse("Usuário cadastrado!")

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login_django(request, user)

            return render(request, 'home.html')
        else:
            return HttpResponse('Email ou senha inválidos')

# @login_required(login_url='/auth/login')
def home(request):
    # if request.user.is_authenticated:
    return render(request, 'home.html')