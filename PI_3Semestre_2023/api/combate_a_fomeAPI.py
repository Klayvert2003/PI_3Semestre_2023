import requests
from bs4 import BeautifulSoup

"""states: AK – Alasca, AL - Alabama, AR - Arkansas, AZ - Arizona, CA - Califórnia, CO - Colorado, CT - Connecticut, DE - Delaware, FL - Flórida, GA - Geórgia, HI - Havaí, IA - Iowa, ID - Idaho, IL - Illinois, IN - Indiana, KS - Kansas, KY - Kentucky, LA - Louisiana, MA - Massachusetts, MD - Maryland, ME - Maine, MI - Michigan, MN - Minnesota, MO - Missouri, MS - Mississippi, MT - Montana, NC - Carolina do Norte, ND - Dakota do Norte, NE - Nebraska, NH - Nova Hampshire, NJ - Nova Jérsei, NM - Novo México, NV - Nevada, NY - Nova Iorque, OH - Ohio, OK - Oklahoma, OR - Oregon, PA - Pensilvânia, RI - Rhode Island, SC - Carolina do Sul, SD - Dakota do Sul, TN - Tennessee, TX - Texas, UT - Utah, VA - Virgínia, VT - Vermont, WA - Washington, WI - Wisconsin, WV - Virgínia Ocidental, WY - Wyoming"""

state = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

headers = {
    'Accept': 'application/xml, text/xml, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,pt;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain',
    'Origin': 'https://www.feedingamerica.org',
    'Referer': 'https://www.feedingamerica.org/find-your-local-foodbank',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

for s in state:
    params = {
        'state': s
    }

    response = requests.get(
        'https://ws2.feedingamerica.org/fawebservice.asmx/GetOrganizationsByState',
        params=params,
        headers=headers,
    )

    if response.status_code == 200:
        try:
            xml_content = response.content
            with open('files/arquivo.xml', 'wb') as f:
                f.write(xml_content)

            soup = BeautifulSoup(xml_content, 'lxml')
            
            zipcode = soup.find_all('zipcode'.split('>')[1])
            agencia = soup.find_all('agencyurl')
            foodbank_name = soup.find_all('fullname')
            print(foodbank_name)

            if zipcode == []:
                print('Não há nenhum food bank para este estado')
            else:
                print(f'A agencia é {agencia}, o nome do local é {foodbank_name} e o CEP é {zipcode}')
        except:
            print('Não foi possível encontar o zip code')
