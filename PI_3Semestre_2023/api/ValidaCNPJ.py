import requests

class ValidaCNPJ():
    def BuscaCNPJ(self, cnpj: str) -> str:
        url = f'https://receitaws.com.br/v1/cnpj/{cnpj}'
        response = requests.get(url).json()
        cep = str(response['cep']).replace('.', '').replace('-', '')
        numero = response['numero']
        complemento = response['complemento']
        telefone = str(response['telefone']).split('/')[0]

        return cep, numero, complemento, telefone