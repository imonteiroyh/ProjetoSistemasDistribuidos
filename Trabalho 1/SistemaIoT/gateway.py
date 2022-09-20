import socket
from config import MULTICAST_PORT, MULTICAST_HOST

HOST = 'localhost'
PORT = 7897

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((MULTICAST_HOST, MULTICAST_PORT))

print('Mensagem enviada')
s.sendto(f'{HOST}:{PORT}'.encode('utf-8'), (MULTICAST_HOST, MULTICAST_PORT))

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((HOST, PORT))

tcp.listen()
print('Esperando dados do sensor...')
conn, add = tcp.accept()


data = conn.recv(1024).decode('utf-8')

sensors = []

sensors.append(data.split(':'))

print(f'sensor adicionado: {data}')