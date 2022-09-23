import socket 
from time import sleep
import struct
from config import GROUP_HOST, GROUP_PORT

HOST = 'localhost'
PORT = 7899

print('Iniciando sensor...')
group_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
group_socket.bind((GROUP_HOST, GROUP_PORT))
group_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mreq = struct.pack("4sl", socket.inet_aton(GROUP_HOST), socket.INADDR_ANY)
group_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
print(f'Comunicação em grupo no endereço {GROUP_HOST}:{GROUP_PORT}')

sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sensor_socket.bind((HOST, PORT))

print('Esperando mensagem de descoberta...')
message = group_socket.recv(1024).decode('utf-8')
gateway_address, gateway_port = message.split(':')
print(f'Gateway identificado: {gateway_address}:{gateway_port}')

sleep(0.5)

print('Conectando ao gateway...')
sensor_socket.connect((gateway_address, int(gateway_port)))
sensor_socket.send(f'{HOST}:{PORT}'.encode('utf-8'))
