import requests
from bs4 import BeautifulSoup

class CEP():
    def pegaCEP():
        cep = ''
        return cep
    
    a = pegaCEP()
    response = requests.get(f'http://viacep.com.br/ws/{a}/json/')

    if response.status_code == 200:
        data = response.json()

        cidade = data["localidade"]
        bairro = data["bairro"]
        rua = data["logradouro"]
        # print(f'A cidade é {cidade}, o bairro é {bairro} e a rua é {rua}')

        with open('core/templates/teste.html', 'r') as file:
            html = file.read()

        soup = BeautifulSoup(html, 'html.parser')

        soup.find('input', {'id': 'rua'}).attrs['value'] = rua
        soup.find('input', {'id': 'bairro'}).attrs['value'] = bairro
        soup.find('input', {'id': 'cidade'}).attrs['value'] = cidade

        with open('core/templates/novo_teste.html', 'w') as file:
            html = file.write(str(soup))
    else:
        print('Não foi possível obter os dados.')
