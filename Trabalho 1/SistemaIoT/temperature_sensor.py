import socket 
from time import sleep
import struct
from config import MULTICAST_HOST, MULTICAST_PORT

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((MULTICAST_HOST, MULTICAST_PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind(('localhost', 7899))

print('Esperando mensagem')
mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_HOST), socket.INADDR_ANY)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
msg = s.recv(1024).decode('utf-8')
host, port = msg.split(':')

sleep(0.5)

tcp.connect((host, int(port)))
tcp.send('localhost:7898'.encode('utf-8'))
