from audioop import add
import socket
from config import GROUP_PORT, GROUP_HOST

HOST = 'localhost'
PORT = 7897

print('Iniciando servidor...')
group_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
group_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
group_socket.bind((GROUP_HOST, GROUP_PORT))
print(f'Comunicação em grupo no endereço {GROUP_HOST}:{GROUP_PORT}')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen()
print(f'Servidor ouvindo no endereço {HOST}:{PORT}')

print('Descobrindo dispositivos...')
group_socket.sendto(f'{HOST}:{PORT}'.encode('utf-8'), (GROUP_HOST, GROUP_PORT))

connection_socket, address = server_socket.accept()
print(f'Conexão aberta: {address}')

data = connection_socket.recv(1024).decode('utf-8')

sensors = []

sensors.append(data.split(':'))

print(f'Sensor adicionado: {data}')