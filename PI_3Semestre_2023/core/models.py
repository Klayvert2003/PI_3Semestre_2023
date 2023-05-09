from django.db import models

class DadosInstituicao(models.Model):
    nome_instituicao = models.CharField('Nome_Instituição', max_length=100)
    cep = models.CharField('CEP', max_length=9)
    cnpj = models.CharField('CNPJ', max_length=14)
    rua = models.CharField('Rua', max_length=100)
    num = models.IntegerField('Número')
    bairro = models.CharField('Bairro', max_length=100)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado', max_length=2)
    latitude = models.CharField('Latitude', max_length=100)
    longitude = models.CharField('Longitude', max_length=100)
    data_hora_cadastro = models.DateTimeField('Data_Hora_Cadastro', auto_now_add=True)

class DadosUsuarios(models.Model):
    nome_usuario = models.CharField('Nome_Usuário', max_length=100)
    cep = models.CharField('CEP', max_length=9)
    rua = models.CharField('Rua', max_length=100)
    num = models.IntegerField('Número')
    bairro = models.CharField('Bairro', max_length=100)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado', max_length=2)
    data_hora_cadastro = models.DateTimeField('Data_Hora_Cadastro', auto_now_add=True)