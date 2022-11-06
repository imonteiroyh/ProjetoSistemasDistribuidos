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


print('Booting smart home system...')
while True:
    print('1 - Air conditioning')
    print('2 - Smart Lamp')
    print('3 - Smart Humidifier')
    device = int(input('Which device do you want to interact with? '))

    if device == 1:
        print('1 - Retrieve the current state of the air conditioning')
        print('2 - Retrieve the current temperature of the air conditioning')
        print('3 - Change the current state of the air conditioning')
        print('4 - Change the current temperature of the air conditioning')
        print('5 - Change the current state of the temperature sensor')
        print('6 - Monitor ambient temperature')
        action = int(input('What do you want to do? '))


        if action == 1:
            request = {'command': 'get_state'}
            raw_response = requests.post(air_conditioner_url, json=request)
            response = loads(raw_response.text)
            print(f'The current state of the air conditioning is {response["state"]}')

        if action == 2:
            request = {'command': 'get_temperature'}
            raw_response = requests.post(air_conditioner_url, json=request)
            response = loads(raw_response.text)
            print(f'The current temperature of the air conditioning is {response["temperature"]} ')

        if action == 3:
            print('1 - Turn off')
            print('2 - Turn on')
            value = int(input('What do you want to do? '))
            if value == 2:
                argument = True
            else:
                argument = False
            request = {
                'command': 'change_state',
                'arguments': argument
                }
            raw_response = requests.post(air_conditioner_url, json=request)
            response = loads(raw_response.text)
            print(response['message'])

        if action == 4:
            temperature = str(input('PWhat temperature do you want to change to?'))
            request = {
                'command': 'change_temperature',
                'arguments' : temperature
                }
            raw_response = requests.post(air_conditioner_url, json=request)
            response = loads(raw_response.text)
            print(response['message'])

        if action == 5:
            print('1 - Turn off')
            print('2 - Turn on')
            value = int(input('What do you want to do? '))
            if value == 2:
                argument = True
            else:
                argument = False
            request = {
                'command': 'change_sensor_state',
                'arguments': argument
                }
            raw_response = requests.post(air_conditioner_url, json=request)
            response = loads(raw_response.text)
            print(response['state'])


        if action == 6:
            while True:
                request = {'command': 'get_sensor_read'}
                raw_response = requests.post(air_conditioner_url, json=request)
                response = loads(raw_response.text)
                print(f'The current temperature of the room is {response["temperature"]} ')
                sleep(3)
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    line = input()
                    break

    if device == 2:
        print('1 - Retrieve the current state of the lamp')
        print('2 - Retrieve current lamp color')
        print('3 - Change the current state of the lamp')
        print('4 - Change the current state of the motion sensor')
        print('5 - Change current lamp color')
        print('6 - Change the current smart mode state')
        print('7 - Monitor de motion sensor')
        action = int(input('What do you want to do? '))

        if action == 1:
            request = {'command': 'get_state'}
            raw_response = requests.post(lamp_url, json=request)
            response = loads(raw_response.text)
            print(f'The current state of the lamp is {response["turned"]}')
        
        if action == 2:
            request = {'command': 'get_color'}
            raw_response = requests.post(lamp_url, json=request)
            response = loads(raw_response.text)
            print(f'The current lamp color is {response["color"]}')
        
        if action == 3:
            print('1 - Turn off')
            print('2 - Turn on')
            index = int(input('What do you want to do? '))
            index = index - 1
            state = str(index)
            print(state)
            request = {
                'command': 'change_state',
                'arguments': state
                }
            raw_response = requests.post(lamp_url, json=request)
            response = loads(raw_response.text)
            print(response['message'])
            

        if action == 4:
            print('1 - Turn off')
            print('2 - Turn on')
            value = int(input('What do you want to do? '))
            if value == 2:
                argument = True
            else:
                argument = False
            request = {
                'command': 'change_sensor_state',
                'arguments': argument
                }
            raw_response = requests.post(air_conditioner_url, json=request)
            response = loads(raw_response.text)
            print(response['state'])

        if action == 5:
            for i in range(0,len(colors_list)):
                print(f'{i+1} - {colors[colors_list[i]]}')
            index = int(input('Which color do you want to change to? '))
            color = colors_list[index-1]
            request = {
                'command': 'change_color',
                'arguments': color
                }
            raw_response = requests.post(lamp_url, json=request)
            response = loads(raw_response.text)
            print(response['message'])
        
        if action == 6:
            print('1 - Turn off')
            print('2 - Turn on')
            index = int(input('What do you want to do? '))
            index = index - 1
            state = str(index)
            print(state)
            request = {
                'command': 'change_smart_lamp_state',
                'arguments': state
                }
            raw_response = requests.post(lamp_url, json=request)
            response = loads(raw_response.text)
            print(response['message'])
        
        if action == 7:
            while True:
                request = {'command': 'get_sensor_read'}
                raw_response = requests.post(lamp_url, json=request)
                response = loads(raw_response.text)
                if response['motion'] == 0:
                    print('The motion sensor did not detect movement')
                elif response['motion'] == 'off':
                    print('The motion sensor is off')
                else:
                    print('The motion detect movement')

                print(response)
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    line = input()
                    break
                sleep(3)



    if device == 3:
        print('1 - Retrieve the current state of the humidifier')
        print('2 - Recuperar se o modo inteligente está ativado')
        print('3 - Recover if smart mode is on')
        print('4 - Change the current smart mode state')
        print('5 - Change Lower Limit and Upper Humidity Limit')
        print('6 - Monitor ambient humidity')
    
        
        action = int(input('What do you want to do? '))

        if action == 1:
            request = {'command': 'get_state'}
            raw_response = requests.post(humidifier_url, json=request)
            response = loads(raw_response.text)
            print(f'The current status of the humidifier is {response["state"]}')
        
        if action == 2:
            request = {'command': 'get_smart_humidifier_state'}
            raw_response = requests.post(humidifier_url, json=request)
            response = loads(raw_response.text)
            print(f'The smart is {response["state"]}')

        if action == 3:
            print('1 - Turn off')
            print('2 - Turn on')
            value = int(input('What do you want to do? '))
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
            print(response['message'])
        
        if action == 4:
            print('1 - Turn off')
            print('2 - Turn on')
            value = int(input('What do you want to do? '))
            if value == 2:
                argument = True
            else:
                argument = False
            request = {
                'command': 'change_smart_humidifier_state',
                'arguments': argument
                }
            raw_response = requests.post(humidifier_url, json=request)
            response = loads(raw_response.text)
            print(response['message'])

        if action == 5:
            inf = int(input('Lower Bound: '))
            sup = int(input('Upper Bound: '))
            request = {
                'command': 'change_bounds',
                'arguments': [inf, sup]
                }
            raw_response = requests.post(humidifier_url, json=request)
            response = loads(raw_response.text)
            print(response['message'])

        if action == 6:
            while True:
                request = {'command': 'get_sensor_read'}
                raw_response = requests.post(humidifier_url, json=request)
                response = loads(raw_response.text)
                print(f'The current humidity in the room is {response["humidity"]} ')
                sleep(3)
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    line = input()
                    break

    print('')