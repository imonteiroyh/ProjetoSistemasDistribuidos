import socket
from config import GROUP_PORT, GROUP_HOST, GATEWAY_PORT
from serializers import message_pb2 as proto
import threading
from time import sleep
import queue

HOST = '127.0.0.1'
PORT = GATEWAY_PORT

all_devices_count = 0

all_devices = {}

def findDevices(group_socket, time=5):
    while True:
        print('Descobrindo dispositivos...')
        message = proto.Message()
        message.type = 'DISCOVER'
        message.discover.CopyFrom(proto.Discover())
        message.discover.ip = HOST
        message.discover.port = PORT
        group_socket.sendto(message.SerializeToString(), (GROUP_HOST, GROUP_PORT))
        sleep(time)


def handleSensor(socket, address, mutex, sensor_id):
    while True:
        f = open("log.txt", 'a')
        data = socket.recv(1024)
        sensor_message = proto.Message()
        sensor_message.ParseFromString(data)

        if sensor_message.type == 'DATA':
            with mutex:
                actual_sensor_state = all_devices[sensor_id]
                actual_sensor_state[0] = [sensor_message.data.data]
                f.write(str(sensor_id) + ': ' + str(all_devices[sensor_id][0][0]) + '\n')
        f.close()


def handleApplication(socket, address, mutex, global_queue):
    while True:
        message = proto.Message(type='DEVICE_LIST')

        devices = []
        for sensor_id in all_devices.keys():
            sensor = all_devices[sensor_id]
            device = proto.Device(id=sensor_id, device_type=sensor[1], communication_type=sensor[2])
            devices.append(device)

        message.device_list.CopyFrom(proto.DeviceList(devices=devices))
        print('Enviando lista de dispositivos...')
        socket.send(message.SerializeToString())

        user_device = proto.Message()
        user_device.ParseFromString(socket.recv(1024))

        if user_device.device.id == 0:
            print('Erro de conexão com a aplicação')
            break

        print(f'Id do dispositivo: {user_device.device.id}')
        print(f'Tipo de dispositivo: {user_device.device.device_type}')

        if user_device.device.communication_type == 'SENSOR':
            while True:
                sleep(2)
                user_data = proto.Message()
                with mutex:
                    user_data.data.CopyFrom(proto.Data(data=all_devices[user_device.device.id][0][0]))
                    #print('enviando...' + str(all_devices[user_device.device.id][0][0]))
                    socket.send(user_data.SerializeToString())
                    server_should_continue = proto.Message()
                    server_should_continue.ParseFromString(socket.recv(1024))
                    if server_should_continue.command.command == 'STOP':
                        break
        else:
            print('Esperando comando...')
            user_command = socket.recv(1024)
            actuator = all_devices[user_device.device.id]
            actuator_socket = actuator[3]
            print('Enviando comando para o atuador...')
            actuator_socket.send(user_command)
            actuator_response = actuator_socket.recv(1024)
            print('Enviando resposta do atuador')
            socket.send(actuator_response)




def handleConnection(socket, address, mutex, global_queue):
    global all_devices_count
    print(f'Conexão aberta: {address}')

    data = socket.recv(1024)

    sensor_response = proto.Message()
    sensor_response.ParseFromString(data)

    if sensor_response.discover.device_type == 'APP':
        handleApplication(socket, address, mutex, global_queue)
        return

    with mutex:
        all_devices_count += 1
        sensor_id = all_devices_count
        if sensor_response.discover.communication_type == 'SENSOR':
            all_devices[sensor_id] = [
                [],
                sensor_response.discover.device_type,
                sensor_response.discover.communication_type
            ]
        else:
            all_devices[sensor_id] = [
                [],
                sensor_response.discover.device_type,
                sensor_response.discover.communication_type,
                socket
            ]

    print(f'Dispositivo adicionado: {sensor_response.discover.device_type}')

    if sensor_response.discover.communication_type == 'SENSOR':
        handleSensor(socket, address, mutex, sensor_id)


print('Iniciando servidor...')
group_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
group_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
group_socket.bind((GROUP_HOST, GROUP_PORT))
print(f'Comunicação em grupo no endereço {GROUP_HOST}:{GROUP_PORT}')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen()
print(f'Servidor ouvindo no endereço {HOST}:{PORT}')

# gateway envia periodicamente ping para todos da lista de sensores/atuadores e quem não responder é tirado da lista

discover_devices_thread = threading.Thread(target=findDevices, args=(group_socket, ))
discover_devices_thread.start()

mutex = threading.Lock()
global_queue = queue.Queue()

while True:
    connection_socket, address = server_socket.accept()
    connection_thread = threading.Thread(target=handleConnection, args=(connection_socket, address, mutex, global_queue))
    connection_thread.start()