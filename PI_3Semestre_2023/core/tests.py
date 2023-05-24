import time
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
                senha.send_keys('123')
                time.sleep(2)
                senhadnv = sc.find_element(By.XPATH, '//input[@id="confirma-senha"]')
                senhadnv.send_keys('123')
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
        self.view_users = kwargs.pop('view_users', False)
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
        for i in range(500, 2500, 500):
            sc.execute_script(f"""window.scrollTo(0, {i})""")
            time.sleep(4)

        sc.execute_script(f"""window.scrollTo(0, 0)""")
        time.sleep(2)

        if self.view_users:
            sc.get(f'{self.address}/info-usuario')

            for i in range(100, 1000, 100):
                sc.execute_script(f"""window.scrollTo(0, {i})""")
                time.sleep(4)

        else:
            associar = sc.find_element(By.XPATH, '//a[@class="btn btn-warning"]')
            associar.click()
            time.sleep(4)

            nome = sc.find_element(By.XPATH, '//input[@id="nome-completo"]')
            time.sleep(2)
            nome.send_keys('Instituição 12')
            time.sleep(2)
            cnpj = sc.find_element(By.XPATH, '//input[@id="cnpj"]')
            cnpj.click()
            cnpj.send_keys(46362661000168)
            time.sleep(2)
            email = sc.find_element(By.XPATH, '//input[@id="email"]')
            email.send_keys('Instituicao12@gmail.com')
            time.sleep(2)
            usuario = sc.find_element(By.XPATH, '//input[@id="usuario"]')
            usuario.send_keys('Instituicao12')
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
                senha.send_keys('123')
                time.sleep(2)
                senhadnv = sc.find_element(By.XPATH, '//input[@id="confirma-senha"]')
                senhadnv.send_keys('123')
                time.sleep(2)
                sc.execute_script(f"""window.scrollTo(0, 200)""")
            
            cadastro = sc.find_element(By.XPATH, '//input[@value="Cadastrar"]')
            cadastro.click()
            time.sleep(5)
            
            alert = sc.switch_to.alert
            alert.accept()
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
                vermapa = sc.find_element(By.XPATH, '//a[@onclick="verMapa(15)"]')
                vermapa.click()

            time.sleep(20)
        # test_case = RegisterInstitutionTest(view_users=True)
        # test_case.test_register_institution()

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
