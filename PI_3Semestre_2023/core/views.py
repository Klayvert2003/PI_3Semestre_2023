from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django
from django.contrib.auth.decorators import login_required
# from core.models import Address
from bs4 import BeautifulSoup
# My functions
from database.conexao import ConexaoMongoDB
from api.correiosAPI import BuscaCEP
from api.GoogleMapsAPI import GoogleMapsAPI

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:   
        email = request.POST.get('email')     
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(email=email).first()

        if user:
            return HttpResponse('Já existe um usuário com este email!!!')
        
        user = User.objects.create_user(username=username, email=email, password=password)

        try: # Tratativa para serviço de MongoDB não inicializado
            credentials = {
                "user": user.username, 
                "email": user.email, 
                "password": user.password,
                "date_joined": user.date_joined
            }
            conexao = ConexaoMongoDB()
            conexao.collection.insert_one(credentials)
        except:
            return HttpResponse("Serviço de MongoDB não inicializado!!!")

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
        
def cep(request):
    if request.method == 'GET':
        return render(request, 'cep.html')
    
    cep = request.POST.get('cep')
    try:
        BuscaCEP.buscar_endereco(cep=cep)
    except:
        return HttpResponse('CEP inválido!!!')

    # Se houver conteúdo no campo cep(e ele for válido)é feita a requisição 
    # então é retornado o html pronto com os dados da API
    if cep:
        return render(request, 'novo_cep.html')
     
def MapsAPI(request, input_address=''):
    if request.method == 'GET':
        return render(request, 'localizacao.html')
    
    client = GoogleMapsAPI()
    input_address = request.POST.get('search')

    try:
        enderecos = client.buscar_endereco(address=input_address)
        # rua = str(enderecos[0]['formatted_address']).split('-')[0]
        # bairro = str(enderecos[0]['formatted_address']).split('-')[1].split(',')[0]
        # cidade = str(enderecos[0]['formatted_address']).split('-')[1].split(',')[1]
        # cep = str(enderecos[0]['formatted_address']).split(',')[2]

        # db_addres = Address(rua=rua, bairro=bairro, cidade=cidade, cep=cep)
        # db_addres.save()

        with open('core/templates/localizacao.html', 'r') as file:
            html = file.read()

            soup = BeautifulSoup(html, 'html.parser')
            soup.find('input', {'id': 'search'}).attrs['value'] = enderecos[0]['formatted_address']

        with open('core/templates/nova_localizacao.html', 'w') as file:
            html = file.write(str(soup.prettify()))

        return render(request, 'nova_localizacao.html')
    except IndexError:
        return HttpResponse('Endereço Inválido')

@login_required(login_url='/auth/login')
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')