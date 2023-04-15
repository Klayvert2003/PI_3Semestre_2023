import requests
import math
from bs4 import BeautifulSoup

class GoogleMapsAPI():
    def __init__(self, api_key='', url='', calcula_distancia=False):
        self.url = url or 'https://maps.googleapis.com/maps/api/geocode/json' # URL requisição
        self.api_key = api_key or 'AIzaSyBeah7e05jIyAyfdwqhwOKobmW56OiFDDE' # Chave da API
        self.calcula_distancia = calcula_distancia # Se for True executa a função CalculaDistancia

        if self.calcula_distancia:
            def CalculaDistancia(address):
                response = requests.get(f"{url}?address={address}&key={api_key}")
                data = response.json()
                lat1 = data['results'][0]['geometry']['location']['lat']
                lon1 = data['results'][0]['geometry']['location']['lng']
                lat2 = -23.5514788
                lon2 = -46.697471

                R = 6371e3  # raio médio da Terra em metros
                phi1 = math.radians(float(lat1))
                phi2 = math.radians(lat2)
                deltaPhi = math.radians(lat2 - float(lat1))
                deltaLambda = math.radians(lon2 - float(lon1))

                a = math.sin(deltaPhi / 2) * math.sin(deltaPhi / 2) + \
                    math.cos(phi1) * math.cos(phi2) * \
                    math.sin(deltaLambda / 2) * math.sin(deltaLambda / 2)
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

                distancia = R * c / 1000
                distancia_aprox = round(distancia, 1)
                print(distancia_aprox)

        else:
            def buscar_endereco(address):
                response = requests.get(f"{self.url}?address={address}&key={self.api_key}")

                if response.status_code == 200:
                    data = response.json()
                    formatted_address = data['results'][0]['formatted_address']
                    
                    with open('../core/templates/localizacao.html', 'r') as file:
                        html = file.read()

                    soup = BeautifulSoup(html, 'html.parser')
                    soup.find('input', {'id': 'search'}).attrs['value'] = formatted_address

                    with open('../core/templates/nova_localizacao.html', 'w') as file:
                        html = file.write(str(soup.prettify()))
                        file.close()
                else:
                    print('Não foi possível obter os dados.')
                return address
                    