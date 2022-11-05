import requests
import sys, select
from json import dumps, loads
from config import HOME_ASSISTANT_PORT, HOST
from time import sleep
BASE_URL = f'http://{HOST}:{HOME_ASSISTANT_PORT}'
air_conditioner_url = f'{BASE_URL}/air_conditioner'
lamp_url = f'{BASE_URL}/lamp'
humidifier_url = f'{BASE_URL}/humidifier'


states = {'on' : 'ligado', 'off' : 'desligado'}


colors_list = ['white', 'red', 'green', 'blue', 'yellow', 'orange', 'cyan']
colors = {'white': 'branco', 'red': 'vermelho', 'green': 'verde', 'blue':'azul',
 'yellow':'amarelo', 'orange':'laranja', 'cyan': 'ciano'}


print('Inicializando sistema de casa inteligente...')
while True:
    print('1 - Ar Condicionado')
    print('2 - Lâmpada Inteligente')
    print('3 - Umidificador Inteligente')
    device = int(input('Com qual dispositivo deseja interagir? '))

    if device == 1:
        print('1 - Recuperar o estado atual do ar-condicionado')
        print('2 - Recuperar a temperatura atual do ar-condicionado')
        print('3 - Mudar o estado atual do ar-condicionado')
        print('4 - Mudar a temperatura do ar-condicionado')
        print('5 - Monitorar temperatura do ambiente')
        action = int(input('O que deseja fazer? '))


        if action == 1:
            request = {'command': 'get_state'}
            raw_response = requests.post(air_conditioner_url, json=request)
            response = loads(raw_response.text)
            print(f'O estado atual do ar-condicionado é {states[response["state"]]}')
            # print(response)

        if action == 2:
            request = {'command': 'get_temperature'}
            raw_response = requests.post(air_conditioner_url, json=request)
            response = loads(raw_response.text)
            print(f'A temperatura atual do ar-condicionado é {response["temperature"]} graus celsius')

        if action == 3:
            print('1 - Desligar')
            print('2 - Ligar')
            value = int(input('O que deseja fazer? '))
            if value == 2:
                argument = 'True'
            else:
                argument = 'False'
            request = {
                'command': 'change_state',
                'arguments': argument
                }
            raw_response = requests.post(air_conditioner_url, json=request)
            response = loads(raw_response.text)
            print(response)

        if action == 4:
            temperature = str(input('Para qual temperatura deseja mudar?'))
            request = {
                'command': 'change_temperature',
                'arguments' : temperature
                }
            raw_response = requests.post(air_conditioner_url, json=request)
            response = loads(raw_response.text)
            print(response)

        if action == 5:
            while True:
                request = {'command': 'get_sensor_read'}
                raw_response = requests.post(air_conditioner_url, json=request)
                response = loads(raw_response.text)
                print(f'A temperatura atual da sala é {response["temperature"]} graus celsius')
                sleep(3)
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    line = input()
                    break

    if device == 2:
        print('1 - Recuperar o estado atual da lâmpada')
        print('2 - Recuperar a cor atual da lâmpada')
        print('3 - Alterar o estado atual da lâmpada')
        print('4 - Alterar a cor atual da lâmpada')
        print('5 - Alterar o estado atual do modo inteligente')
        action = int(input('O que deseja fazer? '))

        if action == 1:
            request = {'command': 'get_state'}
            raw_response = requests.post(lamp_url, json=request)
            response = loads(raw_response.text)
            print(f'O estado atual da lampada é {states[response["turned"]]}')
        
        if action == 2:
            request = {'command': 'get_color'}
            raw_response = requests.post(lamp_url, json=request)
            response = loads(raw_response.text)
            print(f'A cor atual da lâmpada é {colors[response["color"]]}')
        
        if action == 3:
            print('1 - Desligar')
            print('2 - Ligar')
            index = int(input('O que deseja fazer? '))
            index = index - 1
            state = str(index)
            print(state)
            request = {
                'command': 'change_state',
                'arguments': state
                }
            raw_response = requests.post(lamp_url, json=request)
            response = loads(raw_response.text)
            print(response)
            

        if action == 4:
            for i in range(0,len(colors_list)):
                print(f'{i+1} - {colors[colors_list[i]]}')
            index = int(input('Para qual cor deseja mudar? '))
            color = colors_list[index-1]
            request = {
                'command': 'change_color',
                'arguments': color
                }
            raw_response = requests.post(lamp_url, json=request)
            response = loads(raw_response.text)
        
        if action == 5:
            print('1 - Desligar')
            print('2 - Ligar')
            index = int(input('O que deseja fazer? '))
            index = index - 1
            state = str(index)
            print(state)
            request = {
                'command': 'change_smart_lamp_state',
                'arguments': state
                }
            raw_response = requests.post(lamp_url, json=request)
            response = loads(raw_response.text)
            print(response)

    if device == 3:
        print('1 - Recuperar o estado atual da umidificador')
        print('2 - Recuperar se o modo inteligente está ativado')
        print('3 - Alterar o estado atual do umidificador')
        print('4 - Alterar o estado atual do modo inteligente')
        print('5 - Alterar limite inferior e limite superior de umidade')
        print('6 - Monitorar a umidade do ambiente')
    
        
        action = int(input('O que deseja fazer? '))

        if action == 1:
            request = {'command': 'get_state'}
            raw_response = requests.post(humidifier_url, json=request)
            response = loads(raw_response.text)
            print(f'O estado atual do umidificador é {states[response["state"]]}')
        
        if action == 2:
            request = {'command': 'get_smart_humidifier_state'}
            raw_response = requests.post(humidifier_url, json=request)
            response = loads(raw_response.text)
            print(f'O inteligente está {states[response["state"]]}')

        if action == 3:
            print('1 - Desligar')
            print('2 - Ligar')
            value = int(input('O que deseja fazer? '))
            if value == 2:
                argument = 'True'
            else:
                argument = 'False'
            request = {
                'command': 'change_state',
                'arguments': argument
                }
            raw_response = requests.post(humidifier_url, json=request)
            response = loads(raw_response.text)
            print(response)
        
        if action == 4:
            print('1 - Desligar')
            print('2 - Ligar')
            value = int(input('O que deseja fazer? '))
            if value == 2:
                argument = 'True'
            else:
                argument = 'False'
            request = {
                'command': 'change_smart_humidifier_state',
                'arguments': argument
                }
            raw_response = requests.post(humidifier_url, json=request)
            response = loads(raw_response.text)
            print(response)

        if action == 5:
            inf = int(input('Limite inferior: '))
            sup = int(input('Limite superior: '))
            request = {
                'command': 'change_bounds',
                'arguments': [inf, sup]
                }
            raw_response = requests.post(humidifier_url, json=request)
            response = loads(raw_response.text)
            print(response)

        if action == 6:
            while True:
                request = {'command': 'get_sensor_read'}
                raw_response = requests.post(humidifier_url, json=request)
                response = loads(raw_response.text)
                print(f'A umidade atual da sala é {response["humidity"]} ')
                sleep(3)
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    line = input()
                    break

    print('')