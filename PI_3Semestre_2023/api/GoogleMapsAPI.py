import googlemaps
import math
import os

from dotenv import load_dotenv

load_dotenv()
class GoogleMapsAPI():
    def __init__(self, calcula_distancia=False):
        self.calcula_distancia = True if calcula_distancia else False # Se for True executa a função CalculaDistancia

    def buscar_endereco(self, address):
        gmaps = googlemaps.Client(key=os.getenv('API_KEY'))
        geocode_result = gmaps.geocode(address)

        results = []
        for result in geocode_result:
            location = result['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            result_dict = {
                'formatted_address': result['formatted_address'],
                'latitude': latitude,
                'longitude': longitude,
                'location_type': result['geometry']['location_type'],
                'viewport': result['geometry']['viewport'],
                'types': result['types']
            }
            results.append(result_dict)
        return results
    
    def get_address(self, cep):
        data = self.buscar_endereco(address=cep)
        rua = str(data[0]['formatted_address']).split('-')[0].strip()
        bairro = str(data[0]['formatted_address']).split('-')[1].split(',')[0].strip()
        cidade = str(data[0]['formatted_address']).split('-')[1].split(',')[1].strip()
        estado = str(data[0]['formatted_address']).split('-')[2].split(',')[0].strip()

        return rua, bairro, cidade, estado

    def CalculaDistancia(self, address):
        gmaps = googlemaps.Client(key=self.api_key)
        geocode_result = gmaps.geocode(address)

        lat1 = geocode_result['results'][0]['geometry']['location']['lat']
        lon1 = geocode_result['results'][0]['geometry']['location']['lng']
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