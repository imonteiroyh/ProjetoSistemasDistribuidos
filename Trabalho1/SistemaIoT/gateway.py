import socket
from config import GROUP_PORT, GROUP_HOST
from serializers import message_pb2 as proto
import threading
from time import sleep
import queue

HOST = 'localhost'
PORT = 7897

sensors_count = 0

sensors = {
}

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
                actual_sensor_state = sensors[sensor_id]
                actual_sensor_state[0] = [sensor_message.data.data]
                f.write(str(sensor_id) + ': ' + str(sensors[sensor_id][0][0]) + '\n')
        f.close()


def handleActuator(socket, address, mutex, global_queue):
    pass


def handleApplication(global_queue):
    pass


def handleConnection(socket, address, mutex, global_queue):
    global sensors_count
    print(f'Conexão aberta: {address}')

    data = socket.recv(1024)

    sensor_response = proto.Message()
    sensor_response.ParseFromString(data)

    with mutex:
        sensors_count += 1
        sensor_id = sensors_count
        sensors[sensor_id] = [[], sensor_response.discover.device_type]

    print(f'Sensor adicionado: {sensor_response.discover.device_type}') 
    
    if sensor_response.discover.communication_type == 'SENSOR':
        handleSensor(socket, address, mutex, sensor_id)
    else:
        handleActuator(socket, address, mutex, sensor_id)


print('Iniciando servidor...')
group_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
group_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
group_socket.bind((GROUP_HOST, GROUP_PORT))
print(f'Comunicação em grupo no endereço {GROUP_HOST}:{GROUP_PORT}')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen()
print(f'Servidor ouvindo no endereço {HOST}:{PORT}')


discover_devices_thread = threading.Thread(target=findDevices, args=(group_socket, ))
discover_devices_thread.start()

mutex = threading.Lock()
global_queue = queue.Queue()

while True:
    connection_socket, address = server_socket.accept()
    connection_thread = threading.Thread(target=handleConnection, args=(connection_socket, address, mutex, global_queue))
    connection_thread.start()