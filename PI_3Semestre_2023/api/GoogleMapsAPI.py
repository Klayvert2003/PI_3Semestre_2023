import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()
class GoogleMapsAPI():
    def __init__(self):
        self

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
    
    def get_address(self, cep: str):
        data = self.buscar_endereco(address=cep)
        rua = str(data[0]['formatted_address']).split('-')[0].strip()
        bairro = str(data[0]['formatted_address']).split('-')[1].split(',')[0].strip()
        cidade = str(data[0]['formatted_address']).split('-')[1].split(',')[1].strip()
        estado = str(data[0]['formatted_address']).split('-')[2].split(',')[0].strip()
        lat = str(data[0]['latitude'])
        lon = str(data[0]['longitude'])

        return rua, bairro, cidade, estado, lat, lon