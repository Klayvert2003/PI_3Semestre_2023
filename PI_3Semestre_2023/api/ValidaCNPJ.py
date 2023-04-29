import requests
from bs4 import BeautifulSoup

class ValidaCNPJ():
    def __init__(self, cnpj, url='https://cnpj.biz'):
        self.url = url
        self.cnpj = cnpj

    def BuscaCNPJ(self):
        response = self.Requisicao()
    
        soup = BeautifulSoup(response.content, 'html.parser')
        div = soup.find('div', attrs={'class': 'col-left'})
        p = div.find_all('p')

        conteudo = []

        for bs in p:
            b = bs.find('b', attrs={'class': 'copy'})
            if b is None:
                continue
            conteudo.append(b.text)

        result  = {
            'cnpj': conteudo[0],
            'razao_social': conteudo[1],
            'nome_fantasia': conteudo[2],
            'data_abertura': conteudo[3],
            'natureza_juridica': conteudo[5],   
            'cidade': conteudo[8]}
                
        return result
        
    def Requisicao(self):                
        headers = {
            'authority': 'cnpj.biz',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'pt-BR,pt;q=0.9',
            'referer': f'{self.url}/procura/{self.cnpj}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        }

        response = requests.get(f'{self.url}/{self.cnpj}', headers=headers)
        if response.status_code == 200:
            print(f'Buscando dados para o CNPJ: {self.cnpj}')
            return response
        else:
            print(f'Não foi possível encontrar o CNPJ: {self.cnpj}')