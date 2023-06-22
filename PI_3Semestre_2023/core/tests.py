import time
import json

from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

class RegisterUserTest(LiveServerTestCase):
    def __init__(self, *args, **kwargs):
        self.register_user = kwargs.pop('register_user', False)
        self.address = kwargs.pop('address', 'http://127.0.0.1:8000')
        super().__init__(*args, **kwargs)

    def test_register_user(self):
        sc = webdriver.Chrome()
        sc.get(self.address)
        sc.maximize_window()
        time.sleep(3)
        
        instituicao = sc.find_element(By.XPATH, '//a[text()="Doador/Voluntário"]')
        instituicao.click()
        time.sleep(3)
        for i in range(500, 3000, 500):
            sc.execute_script(f"""window.scrollTo(0, {i})""")
            time.sleep(4)
            
        if self.register_user:
            quero_colaborar = sc.find_element(By.XPATH, '//a[@class="btn_quero_doar"]')
            quero_colaborar.click()
            time.sleep(4)
            
            nome = sc.find_element(By.XPATH, '//input[@id="nome-completo"]')
            time.sleep(2)
            nome.send_keys('teste3')
            time.sleep(2)
            cnpj = sc.find_element(By.XPATH, '//input[@id="cep"]')
            cnpj.send_keys(13617060)
            time.sleep(2)
            num = sc.find_element(By.XPATH, '//input[@id="num"]')
            num.send_keys(240)
            time.sleep(2)
            email = sc.find_element(By.XPATH, '//input[@id="email"]')
            email.send_keys('testeusuario3@gmail.com')
            time.sleep(2)
            usuario = sc.find_element(By.XPATH, '//input[@id="usuario"]')
            usuario.send_keys('teste2')
            time.sleep(2)
            try:
                senha = sc.find_element(By.XPATH, '//input[@id="senha"]')
                senha.send_keys('123')
                time.sleep(2)
                senhadnv = sc.find_element(By.XPATH, '//input[@id="confirma-senha"]')
                senhadnv.send_keys('123')
                time.sleep(2)
            except:
                senha = sc.find_element(By.XPATH, '//input[@id="senha"]')
                senha.send_keys('12345678')
                time.sleep(2)
                senhadnv = sc.find_element(By.XPATH, '//input[@id="confirma-senha"]')
                senhadnv.send_keys('12345678')
                time.sleep(2)
                sc.execute_script(f"""window.scrollTo(0, 200)""")    
            finally:
                sc.execute_script(f"""window.scrollTo(0, 200)""")
            time.sleep(2)
            sc.execute_script("""document.querySelector("#submit-button").click()""")
            time.sleep(2)

            alert = sc.switch_to.alert
            alert.accept()
            time.sleep(20)
        
        else:
            sc.get(f'{self.address}/instituicoes')
            time.sleep(4)

            for i in range(500, 3000, 500):
                sc.execute_script(f"""window.scrollTo(0, {i})""")
                time.sleep(4)

            sc.execute_script("""window.scrollTo(0, 0)""")
            time.sleep(2)

            try:
                sc.execute_script("""document.querySelector("#\\31  > button > a").click()""")
                time.sleep(10)
            except:
                sc.execute_script("""window.scrollTo(0, 500)""")
                time.sleep(2)
                vermapa = sc.find_element(By.XPATH, '//a[@onclick="verMapa(15)"]')
                vermapa.click()

            time.sleep(20)
        # test_case = RegisterUserTest(register_user=True)
        # test_case.test_register_user()

    
class RegisterInstitutionTest(LiveServerTestCase):
    def __init__(self, *args, **kwargs):
        self.address = kwargs.pop('address', 'http://127.0.0.1:8000')
        super().__init__(*args, **kwargs)

    def test_register_institution(self):
        sc = webdriver.Chrome()
        sc.get(self.address)
        sc.maximize_window()
        time.sleep(3)
        
        instituicao = sc.find_element(By.XPATH, '//a[text()="Instituição"]')
        instituicao.click()
        time.sleep(3)
        for i in range(500, 2000, 500):
            sc.execute_script(f"""window.scrollTo(0, {i})""")
            time.sleep(4)

        sc.execute_script(f"""window.scrollTo(0, 0)""")
        time.sleep(2)

        cadastro = sc.find_element(By.XPATH, '//a[text()="Cadastro"]')
        cadastro.click()
        time.sleep(4)

        nome = sc.find_element(By.XPATH, '//input[@id="nome-completo"]')
        time.sleep(2)
        nome.send_keys('InstituicaoTeste')
        time.sleep(2)
        cnpj = sc.find_element(By.XPATH, '//input[@id="cnpj"]')
        cnpj.click()
        cnpj.send_keys(46362661000168)
        time.sleep(2)
        email = sc.find_element(By.XPATH, '//input[@id="email"]')
        email.send_keys('InstituicaoTeste@gmail.com')
        time.sleep(2)
        usuario = sc.find_element(By.XPATH, '//input[@id="usuario"]')
        usuario.send_keys('InstituicaoTeste')
        time.sleep(2)
        try:
            senha = sc.find_element(By.XPATH, '//input[@id="senha"]')
            senha.send_keys('123')
            time.sleep(2)
            senhadnv = sc.find_element(By.XPATH, '//input[@id="confirma-senha"]')
            senhadnv.send_keys('123')
            time.sleep(2)
        except:
            senha = sc.find_element(By.XPATH, '//input[@id="senha"]')
            senha.send_keys('12345678')
            time.sleep(2)
            senhadnv = sc.find_element(By.XPATH, '//input[@id="confirma-senha"]')
            senhadnv.send_keys('12345678')
            time.sleep(2)
            sc.execute_script(f"""window.scrollTo(0, 200)""")

        cadastro = sc.find_element(By.XPATH, '//input[@value="Próximo"]').click()
        time.sleep(5)

        # 2º Etapa do Cadastro
        complemento = sc.find_element(By.XPATH, '//input[@id="complemento"]')
        complemento.send_keys('rua exemplo')
        time.sleep(2)

        telefone = sc.find_element(By.XPATH, '//input[@id="telefone"]')
        telefone.send_keys('(19)3571-0471')
        time.sleep(2)

        celular = sc.find_element(By.XPATH, '//input[@id="celular"]')
        celular.send_keys('(19)98602-8206')
        time.sleep(2)

        whatsapp = sc.find_element(By.XPATH, '//label[@class="toggle-container"]').click()
        time.sleep(2)

        descricao = 'Instituição de doação alimentar: Nossa missão é combater a fome, fornecendo alimentos nutritivos e frescos para aqueles em necessidade. Juntos, podemos fazer a diferença!'
        sc.execute_script(f"""document.querySelector("#descreva").value = {json.dumps(descricao)};""")
        time.sleep(2)

        forma1 = sc.find_element(By.XPATH, '//input[@id="doacao1"]')
        forma1.send_keys('Voluntariado aos fins de semana')
        time.sleep(2)

        forma2 = sc.find_element(By.XPATH, '//input[@id="doacao2"]')
        forma2.send_keys('Doação de alimentos')
        time.sleep(2)

        forma3 = sc.find_element(By.XPATH, '//input[@id="doacao3"]')
        forma3.send_keys('Doação de dinheiro')
        time.sleep(2)

        cadastro = sc.find_element(By.XPATH, '//input[@value="Cadastrar Dados"]').click()
        time.sleep(5)

        for i in range(500, 2500, 500):
            sc.execute_script(f"""window.scrollTo(0, {i})""")
            time.sleep(4)

        sc.execute_script("""window.scrollTo(0, 0)""")
        time.sleep(2)

        try:
            sc.execute_script("""document.querySelector("#\\31  > button > a").click()""")
            time.sleep(10)
        except:
            sc.execute_script("""window.scrollTo(0, 500)""")
            time.sleep(2)
            vermapa = sc.find_element(By.XPATH, '//a[@onclick="verMapa(4)"]')
            vermapa.click()
            time.sleep(20)
        # test_case = RegisterInstitutionTest(view_users=True)
        # test_case.test_register_institution()


class CadastroUsuarioTest(LiveServerTestCase):
    def __init__(self, *args, **kwargs):
        self.register_user = kwargs.pop('register_user', False)
        self.address = kwargs.pop('address', 'http://127.0.0.1:8000')
        super().__init__(*args, **kwargs)

    def test_register_user(self):
        #cadastro de usuário
        sc = webdriver.Chrome()
        sc.get(self.address)
        sc.maximize_window()
        time.sleep(3)

        ususario = sc.find_element(By.XPATH, '//a[text()="Doador/Voluntário"]')
        ususario.click()
        time.sleep(3)

        for i in range(500, 3000, 500):
            sc.execute_script(f"""window.scrollTo(0, {i})""")
            time.sleep(2)

        quero_colaborar = sc.find_element(By.XPATH, '//a[@class="btn_quero_doar"]')
        quero_colaborar.click()
        time.sleep(2)

        nome = sc.find_element(By.XPATH, '//input[@id="nome-completo"]')
        time.sleep(2)
        nome.send_keys('teste_cadastro_usuario_automatizado')
        time.sleep(2)

        cep = sc.find_element(By.XPATH, '//input[@id="cep"]')
        cep.send_keys(13617060)
        time.sleep(2)

        num = sc.find_element(By.XPATH, '//input[@id="num"]')
        num.send_keys(240)
        time.sleep(2)

        email = sc.find_element(By.XPATH, '//input[@id="email"]')
        email.send_keys('teste_cadastro_usuario_selenium_automatizado1@gmail.com')
        time.sleep(2)

        usuario = sc.find_element(By.XPATH, '//input[@id="usuario"]')
        usuario.send_keys('teste_cadastro_usuario_automatizado1') 
        time.sleep(2)
        try:
            senha = sc.find_element(By.XPATH, '//input[@id="senha"]')
            senha.send_keys(123)
            time.sleep(2)

            senhadnv = sc.find_element(By.XPATH, '//input[@id="confirma-senha"]')
            senhadnv.send_keys(123)
            time.sleep(2)

            botao = sc.find_element(By.XPATH, '//input[@id="submit-button"]')
            botao.click()
            time.sleep(5)
        except:
            senha = sc.find_element(By.XPATH, '//input[@id="senha"]')
            senha.send_keys(123455678)
            time.sleep(2)

            senhadnv = sc.find_element(By.XPATH, '//input[@id="confirma-senha"]')
            senhadnv.send_keys(123455678)
            time.sleep(2)

            botao = sc.find_element(By.XPATH, '//input[@id="submit-button"]')
            botao.click()
            time.sleep(5)                


        telefone = sc.find_element(By.XPATH, '//input[@id="telefone"]')
        telefone.click()
        time.sleep(2)
        telefone.send_keys(19997961491)
        time.sleep(2)
        celular = sc.find_element(By.XPATH, '//input[@id="celular"]')
        celular.click()
        time.sleep(2)
        celular.send_keys(19997961491)
        time.sleep(2)
        sobre_usuario = sc.find_element(By.XPATH, '//textarea[@id="descreva"]')
        sobre_usuario.click()
        time.sleep(2)
        sobre_usuario.send_keys('Isso é um texto de testes do cadastro do usuário')
        time.sleep(2)
        
        cadastrar_dados = sc.find_element(By.XPATH, '//input[@type="submit" and @value="Cadastrar Dados"]')
        segunda_manha = sc.find_element(By.XPATH, '//input[@id="segunda_manha"]')
        segunda_manha.click()
        time.sleep(2)
        terca_tarde = sc.find_element(By.XPATH, '//input[@id="terca_tarde"]')
        terca_tarde.click()
        time.sleep(2)
        quarta_noite = sc.find_element(By.XPATH, '//input[@id="quarta_noite"]')
        quarta_noite.click() 
        time.sleep(2)
        quinta_tarde = sc.find_element(By.XPATH, '//input[@id="quinta_tarde"]')
        quinta_tarde.click()
        time.sleep(2)

        cadastrar_dados.click()
        time.sleep(5)      
                

class TestLoginEdit(TestCase):
    def setUp(self):
        self.address = 'http://127.0.0.1:8000/index'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_Login_Edit_Contato_user(self):
        self.driver.get(self.address)
        self.driver.implicitly_wait(50)

        # Fazendo login
        menu_hamburguer = self.driver.find_element(By.XPATH, '//label[@for="toggle"]')
        menu_hamburguer.click()
        time.sleep(3)

        Login = self.driver.find_element(By.XPATH, '//a[text()="Login"]')
        Login.click()
        self.driver.implicitly_wait(50)

        username = self.driver.find_element(By.XPATH, '//input[@id="username"]')
        username.click()
        username.send_keys('teste_cadastro_usuario_automatizado')
        time.sleep(2)
        try: 
            password = self.driver.find_element(By.XPATH, '//input[@id="password"]')        
            password.click()
            password.send_keys(123)
        except: 
            password = self.driver.find_element(By.XPATH, '//input[@id="password"]')        
            password.click()
            password.send_keys(12345678)

        botao = self.driver.find_element(By.CSS_SELECTOR, ".login-box-enviar")
        botao.click()
        time.sleep(3)

        menu_hamburguer = self.driver.find_element(By.XPATH, '//label[@for="toggle"]')
        menu_hamburguer.click()
        time.sleep(3)

        Edit = self.driver.find_element(By.XPATH, '//a[text()="Edit"]')
        Edit.click()
        time.sleep(3)

        complemento = self.driver.find_element(By.XPATH, '//input[@id="complemento"]')
        complemento.click()
        time.sleep(3)
        complemento.clear()
        complemento.send_keys('teste123')
        time.sleep(3)

        botao = self.driver.find_element(By.XPATH, '//input[@type="submit" and @value="Salvar Dados"]')
        botao.click()
        time.sleep(3)

class TestSobreContato(TestCase):
    def setUp(self):
        self.address = 'http://127.0.0.1:8000/index'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_Login_Edit_Contato_user(self):
        self.driver.get(self.address)
        self.driver.implicitly_wait(50)

    # Mostrando a aba contato
        label_element = self.driver.find_element(By.XPATH, '//label[@for="toggle"]')
        label_element.click()
        time.sleep(3)

        passeio = self.driver.find_element(By.XPATH, '//a[text()="Contato"]')
        passeio.click()
        self.driver.implicitly_wait(50)
        time.sleep(3)

        name = self.driver.find_element(By.XPATH, '//input[@id="name"]')
        name.click()
        name.send_keys('teste_cadastro_usuario2')
        time.sleep(3)

        email = self.driver.find_element(By.XPATH, '//input[@id="email"]')        
        email.click()
        email.send_keys('teste_cadastro_usuario2@testecadastrousuario2.com')
        time.sleep(3)

        message = self.driver.find_element(By.XPATH, '//textarea[@id="message"]')
        message.click()
        message.send_keys('isso aqui é um teste')
        time.sleep(3)

        button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        button.click()
        time.sleep(3)

        #mostrando a aba sobre
        label_elementdnv = self.driver.find_element(By.XPATH, '//label[@for="toggle"]')
        label_elementdnv.click()
        time.sleep(3)

        sobre = self.driver.find_element(By.XPATH, '//a[text()="Sobre"]')
        sobre.click()
        self.driver.implicitly_wait(50)
        time.sleep(3)
        for i in range(500, 3000, 500):
            self.driver.execute_script(f"""window.scrollTo(0, {i})""")
            time.sleep(2)

        btn = self.driver.find_element(By.XPATH, '//a[text()="Doe e faça história"]')
        btn.click()
        time.sleep(3)

class StatusCodeHomeUsuarioTestCase(TestCase):
    def setUp(self):
        self.resp = self.client.get('/home-usuario')

    def test_200_response_HomeUsuario(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template_HomeUsuario(self):
        self.assertTemplateUsed(self.resp, 'home-usuario.html')   

class StatusCodeHomeInstituicoesTestCase(TestCase):
    def setUp(self):
        self.resp = self.client.get('/instituicoes')

    def test_200_response_Instituicoes(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template_Instituicoes(self):
        self.assertTemplateUsed(self.resp, 'instituicoes.html')    

class StatusCodeLoginTestCase(TestCase):
    def setUp(self):
        self.resp = self.client.get('/login')

    def test_200_response_Login(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template_Login(self):
        self.assertTemplateUsed(self.resp, 'login.html')   

class StatusCodeCadastroUsuarioTestCase(TestCase):
    def setUp(self):
        self.resp = self.client.get('/cadastro-usuario')

    def test_200_response_CadastroUsuario(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template_CadastroUsuario(self):
        self.assertTemplateUsed(self.resp, 'cadastro-usuario.html')     

class StatusCodeCadastroInstituicaoTestCase(TestCase):
    def setUp(self):
        self.resp = self.client.get('/cadastro-instituicao')

    def test_200_response_CadastroInstituicao(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template_CadastroInstituicao(self):
        self.assertTemplateUsed(self.resp, 'cadastro-instituicao.html')      

class StatusCodeIndexTestCase(TestCase):
    def setUp(self):
        self.resp = self.client.get('/index')

    def test_200_response_Index(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template_Index(self):
        self.assertTemplateUsed(self.resp, 'index.html')      
