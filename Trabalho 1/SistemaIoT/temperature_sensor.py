from re import S
import socket 
from config import MULTICAST_HOST, MULTICAST_PORT

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((MULTICAST_HOST, MULTICAST_PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind(('localhost', 7898))

print('Esperando mensagem')
msg = s.recv(1024).decode('utf-8')
host, port = msg.split(':')

tcp.connect((host, port))
tcp.send('localhost:7898'.encode('utf-8'))
