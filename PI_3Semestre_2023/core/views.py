# External libs
import json

# Django libs
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

# Páginas comuns
class Index(View):
    def get(self, request):
        return render(request, 'index.html')

class HomeUsuarios(TemplateView):
    def get(self, request):
        template_name = 'home-usuario.html'
        return render(request, template_name)
        
    def post(self, request):
        return render(request, 'instituicoes.html')

class HomeInstituicao(TemplateView):
    def get(self, request):
        template_name='lp_instituicao.html'
        return render(request, template_name)


class ContatoView(TemplateView):
    def get(self, request):
        template_name='contato.html'
        return render(request, template_name)

class SobreView(TemplateView):
    def get(self, request):
        template_name='sobre.html'
        return render(request, template_name)

# Retorna os dados do banco para renderizar o mapa na página seguinte
class InstituicoesView(GoogleMapsAPI, View):
    def get(self, request):
        dados = list(DadosInstituicao.objects.all().values('id', 'nome_instituicao', 'latitude', 'longitude', 'descricao'))

        return render(request, 'instituicoes.html', {'dados': dados})

    def post(self):
        return redirect('card-map')

# Renderiza o mapa com base nos dados enviados na URL da view acima
class CardMapView(View):
    def get(self, request):
        lat = request.GET.get('latitude', None)
        lon = request.GET.get('longitude', None)
        id_instituicao = request.GET.get('id', None)
        dados = DadosInstituicao.objects.get(id=id_instituicao)

        data = {
            'nome_instituicao': dados.nome_instituicao,
            'cnpj': dados.cnpj,
            'descricao': dados.descricao,
            'forma_ajuda1': dados.forma_ajuda1,
            'forma_ajuda2': dados.forma_ajuda2,
            'forma_ajuda3': dados.forma_ajuda3
        }

        if lat and lon:
            return render(request, 'card-map.html', {'latitude': lat, 'longitude': lon, 'API_KEY': API_KEY, 'dados': data})
        else:
            return redirect('instituicoes')

# Página que retorna uma tabela com as informações de todos os contatos cadastrados no sistema 
class ListaContato(TemplateView):
    template_name = 'lista-contato.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dados = DadosUsuarios.objects.all().values('nome_usuario', 'email', 'cel', 'disponibilidade')

        contatos_serializados = []
        for contato in dados:
            dias_disponiveis = []

        disponibilidade = contato['disponibilidade']
        if disponibilidade is not None:
            for dia, horarios in contato['disponibilidade'].items():
                horarios_disponiveis = [horario for horario, disponivel in horarios.items() if disponivel]
                if horarios_disponiveis:
                    dias_disponiveis.append({
                        'dia': dia,
                        'horarios': horarios_disponiveis
                    })

            periodo_disponivel = ""
            for dia in dias_disponiveis:
                nome_dia = dia['dia']
                horarios = ", ".join(dia['horarios'])
                periodo_disponivel += f"{nome_dia} no(s) período(s) da(s) {horarios}. "

            contato_dict = {
                'nome_usuario': contato['nome_usuario'],
                'email': contato['email'],
                'cel': contato['cel'],
                'periodo_disponivel': periodo_disponivel
            }
            contatos_serializados.append(contato_dict)

        with open('core/static/json/dados.json', 'w') as arquivo_json:
            json.dump(contatos_serializados, arquivo_json)

        context['contatos'] = contatos_serializados
        return context

# Etapa inicial do registro de instituição
class CadastroInstituicaoView(ValidaCNPJ, GoogleMapsAPI, View):
    def get(self, request):
        return render(request, 'cadastro-instituicao.html')
        
    def post(self, request):
        email = request.POST.get('email')
        usuario = request.POST.get('usuario')
        password = request.POST.get('senha')
        confirm_password = request.POST.get('confirma-senha')
        infos = None
        nome_instituicao = request.POST.get('nome-completo')
        cnpj = request.POST.get('cnpj')
        if cnpj:
            try:
                cnpj = str(cnpj).replace('.', '').replace('-', '').replace('/', '')
                try:
                    infos = self.BuscaCNPJ(cnpj=cnpj)
                    address = self.get_complete_address(cep=infos[0], num=infos[1])
                except TypeError:
                    if not infos:
                        messages.error(request, 'CNPJ inválido!!!')
                        return render(request, 'cadastro-instituicao.html',
                            {'nome_instituicao': nome_instituicao, 'cnpj': cnpj, 
                             'email': email, 'usuario': usuario})
            except AttributeError:
                messages.error(request, 'CNPJ Inválido!!!')
                return render(request, 'cadastro-instituicao.html',
                            {'nome_instituicao': nome_instituicao, 'cnpj': cnpj, 
                             'email': email, 'usuario': usuario})
            
        user = User.objects.filter(email=email).first()
        if user:
            messages.warning(request, 'Já existe um usuário com este email!!!')
            return render(request, 'cadastro-instituicao.html',
                            {'nome_instituicao': nome_instituicao, 'cnpj': cnpj, 
                             'email': email, 'usuario': usuario})
        
        if password != confirm_password:
            messages.warning(request, 'Senhas divergentes!!!')
            return render(request, 'cadastro-instituicao.html',
                            {'nome_instituicao': nome_instituicao, 'cnpj': cnpj, 
                             'email': email, 'usuario': usuario})
        elif len(password) < 8 and len(confirm_password) < 8:
            messages.warning(request, 'Senha fraca! Digite ao menos 8 caracteres!')
            return render(request, 'cadastro-instituicao.html',
                            {'nome_instituicao': nome_instituicao, 'cnpj': cnpj, 
                             'email': email, 'usuario': usuario})
        
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
        request.session['etapa1_instituicao_concluida'] = True
        return render(request, 'detalhes-instituicao.html', {'dados': data})

# Segunda etapa do registro da instituição
class DetalhesInstituicao(GoogleMapsAPI, ValidaCNPJ, View):
    def get(self, request):
        if not request.session.get('etapa1_instituicao_concluida'):
            return redirect('cadastro-instituicao')
        template_name = 'detalhes-instituicao.html'
        return render(request, template_name)

    def post(self, request):
        if not request.session.get('etapa1_instituicao_concluida'):
            return redirect('cadastro-instituicao')
        email = request.session.get('email')
        usuario = request.session.get('usuario')
        senha = request.session.get('senha')
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
        address = None
        if cnpj:
            try:
                infos = self.BuscaCNPJ(cnpj=cnpj)
                address = self.get_complete_address(cep=infos[0], num=infos[1])
            except TypeError:
                if not infos:
                    messages.error(request, 'CNPJ inválido!!!')
                    return redirect('detalhe-instituicao')
            except AttributeError:
                messages.error(request, 'CNPJ Inválido!!!')
                return render(request, 'detalhe-instituicao')
        descricao = request.POST.get('descreva')
        forma_ajuda1 = request.POST.get('doacao1')
        forma_ajuda2 = request.POST.get('doacao2')
        forma_ajuda3 = request.POST.get('doacao3')
        user = User.objects.filter(email=email).first()
        if user:
            messages.warning(request, 'Já existe um usuário com este email!!!')
            return redirect('detalhe-instituicao')

        address = self.valida_address(cep, num)
        if not address:
            messages.error(request, 'Endereço incorreto!!!')
            data = {
                'nome_instituicao': nome_instituicao,
                'cep': cep,
                'rua': rua,
                'num': num,
                'bairro': bairro,
                'cidade': cidade,
                'complemento': complemento,
                'estado': estado,
                'tel': tel,
                'cel': cel
            }
            return render(request, 'detalhes-instituicao.html', {'dados': data})

        user = User.objects.create_user(username=usuario, email=email, password=senha)
        
        DadosInstituicao.objects.create(id=user.id, email=email, cel=cel, tel=tel, descricao=descricao, forma_ajuda1=forma_ajuda1, 
        forma_ajuda2=forma_ajuda2, forma_ajuda3=forma_ajuda3, nome_instituicao=nome_instituicao, 
        cep=cep, num=num, cnpj=cnpj, rua=rua, complemento=complemento, bairro=bairro, cidade=cidade, 
        estado=estado, latitude=address[4], longitude=address[5])

        messages.success(request, 'Instituição Cadastrada com Sucesso!!!')
        
        return redirect('instituicoes')

# Etapa inicial do cadastro de um usuário doador/voluntário
class CadastroUsuarioView(GoogleMapsAPI, View):
    def get(self, request):
        return render(request, 'cadastro-usuario.html')
    
    def post(self, request):
        nome_completo = request.POST.get('nome-completo')     
        cep = request.POST.get('cep')
        num = request.POST.get('num')
        email = request.POST.get('email')
        usuario = request.POST.get('usuario')
        password = request.POST.get('senha')
        confirm_password = request.POST.get('confirma-senha')
        address = None
        if cep and num:
            try:
                cep = str(cep).replace('-', '').replace('.', '')
                try:
                    address = self.get_complete_address(cep, str(num))
                except TypeError:
                    if not address:
                        messages.error(request, 'CEP ou número inválidos!!!')
                        return render(
                            request, 'cadastro-usuario.html', {'nome_completo': nome_completo, 
                                     'cep': cep, 'num': num, 'email': email, 'usuario': usuario})
            except IndexError:
                messages.error(request, 'CEP ou número inválidos!!!')
                return redirect('cadastro-usuario')

        user = User.objects.filter(email=email).first()
        if user:
            messages.warning(request, 'Já existe um usuário com este email!!!')
            return render(
                request, 'cadastro-usuario.html', {'nome_completo': nome_completo, 
                         'cep': cep, 'num': num, 'email': email, 'usuario': usuario})
        
        if password != confirm_password:
            messages.warning(request, 'Senhas divergentes!!!')
            return render(
                request, 'cadastro-usuario.html', {'nome_completo': nome_completo, 
                         'cep': cep, 'num': num, 'email': email, 'usuario': usuario})
        
        data = {
            'usuario': usuario,
            'senha': password,
            'email': email,
            'nome_completo': nome_completo,
            'cep': cep,
            'num': num,
            'rua': address[0],
            'bairro': address[1],
            'cidade': address[2],
            'estado': address[3]
        }

        request.session['email'] = email
        request.session['usuario'] = usuario
        request.session['senha'] = password
        request.session['etapa1_usuario_concluida'] = True
        return render(request, 'Informacoes_de_usuario.html', {'dados': data})

# Segunda etapa do cadastro de um usuário doador/voluntário
class DetalhesUsuario(GoogleMapsAPI, View):
    def get(self, request):
        if not request.session.get('etapa1_usuario_concluida'):
            return redirect('cadastro-usuario')
        return render(request, 'Informacoes_de_usuario.html')
    
    def post(self, request):
        if not request.session.get('etapa1_usuario_concluida'):
            return redirect('cadastro-usuario')
        email = request.session.get('email')
        usuario = request.session.get('usuario')
        senha = request.session.get('senha')
        nome_completo = request.POST.get('nome-completo')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        num = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        complemento = request.POST.get('complemento')
        estado = request.POST.get('estado')
        tel = request.POST.get('telefone')
        cel = request.POST.get('celular')
        segunda_manha = request.POST.getlist('segunda_manha')
        segunda_tarde = request.POST.getlist('segunda_tarde')
        segunda_noite = request.POST.getlist('segunda_noite')
        terca_manha = request.POST.getlist('terca_manha')
        terca_tarde = request.POST.getlist('terca_tarde')
        terca_noite = request.POST.getlist('terca_noite')
        quarta_manha = request.POST.getlist('quarta_manha')
        quarta_tarde = request.POST.getlist('quarta_tarde')
        quarta_noite = request.POST.getlist('quarta_noite')
        quinta_manha = request.POST.getlist('quinta_manha')
        quinta_tarde = request.POST.getlist('quinta_tarde')
        quinta_noite = request.POST.getlist('quinta_noite')
        sexta_manha = request.POST.getlist('sexta_manha')
        sexta_tarde = request.POST.getlist('sexta_tarde')
        sexta_noite = request.POST.getlist('sexta_noite')
        sabado_manha = request.POST.getlist('sabado_manha')
        sabado_tarde = request.POST.getlist('sabado_tarde')
        sabado_noite = request.POST.getlist('sabado_noite')
        domingo_manha = request.POST.getlist('domingo_manha')
        domingo_tarde = request.POST.getlist('domingo_tarde')
        domingo_noite = request.POST.getlist('domingo_noite')

        disponibilidades = {
            'segunda': {
                'manha': bool(segunda_manha),
                'tarde': bool(segunda_tarde),
                'noite': bool(segunda_noite),
            },
            'terca': {
                'manha': bool(terca_manha),
                'tarde': bool(terca_tarde),
                'noite': bool(terca_noite),
            },
            'quarta': {
                'manha': bool(quarta_manha),
                'tarde': bool(quarta_tarde),
                'noite': bool(quarta_noite),
            },
            'quinta': {
                'manha': bool(quinta_manha),
                'tarde': bool(quinta_tarde),
                'noite': bool(quinta_noite),
            },
            'sexta': {
                'manha': bool(sexta_manha),
                'tarde': bool(sexta_tarde),
                'noite': bool(sexta_noite),
            },
            'sabado': {
                'manha': bool(sabado_manha),
                'tarde': bool(sabado_tarde),
                'noite': bool(sabado_noite),
            },
            'domingo': {
                'manha': bool(domingo_manha),
                'tarde': bool(domingo_tarde),
                'noite': bool(domingo_noite),
            },
        }
        address = None
        if cep and num:
            try:
                cep = str(cep).replace('-', '').replace('.', '')
                try:
                    address = self.get_complete_address(cep, str(num))
                except TypeError:
                    if not address:
                        messages.error(request, 'CEP ou número inválidos!!!')
                        return render(
                            request, 'Informacoes_de_usuario.html', {'nome_completo': nome_completo, 
                                     'cep': cep, 'num': num, 'email': email, 'usuario': usuario})
            except IndexError:
                messages.error(request, 'CEP ou número inválidos!!!')
                return redirect('detalhe-usuario')

        address = self.valida_address(cep, num)
        if not address:
            messages.error(request, 'Endereço incorreto!!!')
            data = {
                'nome_completo': nome_completo,
                'cep': cep,
                'rua': rua,
                'num': num,
                'bairro': bairro,
                'cidade': cidade,
                'complemento': complemento,
                'estado': estado,
                'tel': tel,
                'cel': cel
            }
            return render(request, 'Informacoes_de_usuario.html', {'dados': data})

        user = User.objects.create_user(username=usuario, email=email, password=senha)

        DadosUsuarios.objects.create(id=user.id, nome_usuario=nome_completo, email=email, cep=cep, 
        num=num,rua=address[0], bairro=address[1], cidade=address[2], estado=address[3], 
        disponibilidade=disponibilidades, tel=tel, cel=cel, complemento=complemento)

        messages.success(request, 'Usuário Cadastrado com Sucesso!!!')
        
        return redirect('home-usuario')

# CRUD
# Página de login
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
            messages.success(request, 'Usuário autenticado!!!')
            return render(request, 'home-usuario.html', {'user_id': user_id})
        else:
            messages.error(request, 'Email ou senha inválidos!!!')
            return render(request, 'login.html')

# Página de Logout
class LogoutView(TemplateView):
    def get(self, request):
        messages.success(request, 'Logout Realizado!!!')
        logout(request)
        return redirect('index')

# Classe que deleta o usuário(ou instituição)
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
                messages.success(request, 'Usuário deletado com sucesso!!!')
                auth_user.delete()

        return redirect('index')

# Classe que edita os dados do usuário(ou instituição)
class EditarUsuario(View):
    def get(self, request):
        instituicao = None
        usuario = None
        id_usuario = request.session.get('user_id')
        dados_usuarios = {}
        dados_instituicao = {}
        try:
            try:
                usuario = DadosUsuarios.objects.get(id=id_usuario)
                dados_usuarios = {
                    'nome': usuario.nome_usuario,
                    'email': usuario.email,
                    'cep': usuario.cep,
                    'num': usuario.num,
                    'rua': usuario.rua,
                    'bairro': usuario.bairro,
                    'cidade': usuario.cidade,
                    'estado': usuario.estado,
                }
            except DadosUsuarios.DoesNotExist:
                print("Usuário não é doador/voluntário.")
                pass
            try:
                instituicao = DadosInstituicao.objects.get(id=id_usuario)
                dados_instituicao = {
                    'usuario': request.session.get('usuario'),
                    'senha': request.session.get('senha'),
                    'email': instituicao.email,
                    'nome': instituicao.nome_instituicao,
                    'cnpj': instituicao.cnpj,
                    'cep': instituicao.cep,
                    'num': instituicao.num,
                    'complemento': instituicao.complemento,
                    'tel': instituicao.tel,
                    'cel': instituicao.cel,
                    'rua': instituicao.rua,
                    'bairro': instituicao.bairro,
                    'cidade': instituicao.cidade,
                    'estado': instituicao.estado,
                    'descricao': instituicao.descricao,
                    'forma_ajuda1': instituicao.forma_ajuda1,
                    'forma_ajuda2': instituicao.forma_ajuda2,
                    'forma_ajuda3': instituicao.forma_ajuda3,
                }
            except DadosInstituicao.DoesNotExist:
                print("Usuário não é uma instituição.")
                pass
        finally:
            return render(request, 'editar-usuario.html', {'dados_usuarios': dados_usuarios, 'dados_instituicao': dados_instituicao})
       
    def post(self, request):
        id_usuario = request.session.get('user_id')
        usuario = None
        instituicao = None
        
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        cep = request.POST.get('cep')
        num = request.POST.get('numero')
        complemento = request.POST.get('complemento')
        tel = request.POST.get('telefone')
        cel = request.POST.get('celular')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        descricao = request.POST.get('descreva')
        forma_ajuda1 = request.POST.get('doacao1')
        forma_ajuda2 = request.POST.get('doacao2')
        forma_ajuda3 = request.POST.get('doacao3')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        numero = request.POST.get('numero')

        try:
            try:
                usuario = DadosUsuarios.objects.get(id=id_usuario)
                usuario.email = email
                usuario.nome_usuario = nome
                usuario.cep = cep
                usuario.num = num
                usuario.complemento = complemento
                usuario.tel = tel
                usuario.cel = cel
                usuario.rua = rua
                usuario.bairro = bairro
                usuario.cidade = cidade
                usuario.estado = estado
                usuario.save()
            except DadosUsuarios.DoesNotExist:
                print("Usuário não é doador/voluntário.")
                pass
            try:
                instituicao = DadosInstituicao.objects.get(id=id_usuario)
                instituicao.email = email
                instituicao.nome_instituicao = nome
                instituicao.cnpj = cnpj
                instituicao.cep = cep
                instituicao.num = num
                instituicao.complemento = complemento
                instituicao.tel = tel
                instituicao.cel = cel
                instituicao.rua = rua
                instituicao.bairro = bairro
                instituicao.cidade = cidade
                instituicao.estado = estado
                instituicao.descricao = descricao
                instituicao.forma_ajuda1 = forma_ajuda1
                instituicao.forma_ajuda2 = forma_ajuda2
                instituicao.forma_ajuda3 = forma_ajuda3
                instituicao.save()
            except DadosInstituicao.DoesNotExist:
                print("Usuário não é uma instituição.")
                pass
        finally:
            messages.success(request, 'Usuário editado com sucesso!!!')
            return redirect('home-usuario')