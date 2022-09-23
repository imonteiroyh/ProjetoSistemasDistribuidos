import socket 
from time import sleep
import struct
from config import GROUP_HOST, GROUP_PORT
from serializers import message_pb2 as proto

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
gateway_discover = proto.Message()
gateway_discover.ParseFromString(group_socket.recv(1024))

if gateway_discover.type == 'DISCOVER':
    discover_message = gateway_discover.discover

print(f'Gateway identificado: {discover_message.ip}:{discover_message.port}')

sleep(0.5)

print('Conectando ao gateway...')
response_discover = proto.Discover()
response_discover.device_type = 'TEMPERATURE_SENSOR'
response_discover.ip = HOST
response_discover.port = PORT

response = proto.Message()
response.type = 'DISCOVER'
response.discover.CopyFrom(response_discover)

sensor_socket.connect((discover_message.ip, discover_message.port))
sensor_socket.send(response.SerializeToString())
