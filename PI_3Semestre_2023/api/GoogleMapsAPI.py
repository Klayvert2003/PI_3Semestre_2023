import googlemaps
# from PI_3Semestre_2023.settings import API_KEY
class GoogleMapsAPI():
    def __buscar_endereco(self, address):
        gmaps = googlemaps.Client(key='API')
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
    
    def __get_address(self, cep: str):
        data = self.__buscar_endereco(address=cep)
        try:
            rua = str(data[0]['formatted_address']).split('-')[0].strip()
            bairro = str(data[0]['formatted_address']).split('-')[1].split(',')[0].strip()
            cidade = str(data[0]['formatted_address']).split('-')[1].split(',')[1].strip()
            estado = str(data[0]['formatted_address']).split('-')[2].split(',')[0].strip()
            lat = str(data[0]['latitude'])
            lon = str(data[0]['longitude'])
            return rua, bairro, cidade, estado, lat, lon
        except:
            return False

    
    def get_complete_address(self, cep: str, num: str):
        data = self.__get_address(cep=cep)
        complete_address = f'{data[0]}, {num}, {data[1]}, {data[2]} - {data[3]}'
        address = GoogleMapsAPI().__buscar_endereco(address=complete_address)
        try:
            rua = str(address[0]['formatted_address']).split('-')[0].strip()
            bairro = str(address[0]['formatted_address']).split('-')[1].split(',')[0].strip()
            cidade = str(address[0]['formatted_address']).split('-')[1].split(',')[1].strip()
            estado = str(address[0]['formatted_address']).split('-')[2].split(',')[0].strip()
            lat = str(address[0]['latitude'])
            lon = str(address[0]['longitude'])

            return rua, bairro, cidade, estado, lat, lon
        except:
            return False
    
    def valida_address(self, cep: str, num: str):
        try:
            data = self.__get_address(cep=cep)
            complete_address = f'{data[0]}, {num}, {data[1]}, {data[2]} - {data[3]}'
            address = GoogleMapsAPI().__buscar_endereco(address=complete_address)
            return self.get_complete_address(cep, num)
        except:
            return False