from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django
from database.conexao import ConexaoMongoDB
from api.correiosAPI import BuscaCEP

conexao = ConexaoMongoDB()

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

            return HttpResponse('Autenticado')
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