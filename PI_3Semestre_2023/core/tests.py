from django.test import TestCase

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
