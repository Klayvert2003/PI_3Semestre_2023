from django.db import models

class Address(models.Model):
    nome_instituicao = models.CharField('Nome_Instituição', max_length=100)
    cnpj = models.IntegerField('CNPJ', max_length=18)
    cep = models.IntegerField('CEP')
    rua = models.CharField('Rua', max_length=100)
    numero = models.IntegerField('Número')
    bairro = models.CharField('Bairro', max_length=100)
    cidade = models.CharField('Cidade', max_length=100)
    complemento = models.CharField('Complemento', max_length=100)
    estado = models.CharField('Estado', max_length=100)
    data_hora_cadastro = models.DateTimeField('Data_Hora_Cadastro', auto_now_add=True)