from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django
from core.static.conexao import ConexaoMongoDB

conexao = ConexaoMongoDB()

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:   
        email = request.POST.get('email')     
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Já existe um usuário com este username!!!')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        credentials = {"user": user.username, "email": user.email, "password": user.password}
        conexao.collection.insert_one(credentials)

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