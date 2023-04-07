from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django
from database.conexao import ConexaoMongoDB
from PI_3Semestre_2023.api.correiosAPI import CEP

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
    cep = request.POST.get('cep')
    a = CEP.pegaCEP()
    if request.method == 'GET':
        return render(request, 'teste.html')

def a(request):
    if request.method == 'GET':
        return render(request, 'novo_teste.html')