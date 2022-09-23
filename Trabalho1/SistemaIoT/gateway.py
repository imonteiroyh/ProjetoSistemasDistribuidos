import socket
from config import GROUP_PORT, GROUP_HOST
from serializers import message_pb2 as proto

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

message = proto.Message()
message.type = 'DISCOVER'
message.discover.CopyFrom(proto.Discover())
message.discover.ip = HOST
message.discover.port = PORT

print('Descobrindo dispositivos...')
group_socket.sendto(message.SerializeToString(), (GROUP_HOST, GROUP_PORT))

connection_socket, address = server_socket.accept()
print(f'Conexão aberta: {address}')

data = connection_socket.recv(1024)

sensor_response = proto.Message()
sensor_response.ParseFromString(data)

print(f'Sensor adicionado: {sensor_response.discover.device_type}')