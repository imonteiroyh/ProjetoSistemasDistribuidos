import requests
from json import dumps, loads
from config import HOME_ASSISTANT_PORT, HOST

BASE_URL = f'http://{HOST}:{HOME_ASSISTANT_PORT}'
air_conditioner_url = f'{BASE_URL}/air_conditioner'

print('Inicializando sistema de casa inteligente...')
print('1 - Ar Condicionado')
device = int(input('Com qual dispositivo deseja interagir? '))

if device == 1:
    print('1 - Recuperar temperatura atual do ar-condicionado')
    print('2 - Mudar temperatura do ar-condicionado')
    print('3 - Monitorar temperatura do ambiente')
    action = int(input('O que deseja fazer? '))

    if action == 1:
        request = {'command': 'get_temperature'}
        raw_response = requests.post(air_conditioner_url, json=request)
        response = loads(raw_response.text)
        print(f'A temperatura atual do ar-condicionado é {response["temperature"]} graus celsius')

    if action == 2:
        temperature = str(input('Para qual temperatura deseja mudar?'))
        request = {'command': 'change_temperature',
                    'arguments' : temperature }
        raw_response = requests.post(air_conditioner_url, json=request)
        response = loads(raw_response.text)
        print(response)