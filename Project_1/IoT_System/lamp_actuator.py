from email import message_from_bytes
import socket
from serializers import message_pb2 as proto
import struct
from config import GROUP_PORT, GROUP_HOST, find_free_port
import sys

HOST = '127.0.0.1'
PORT = find_free_port() if len(sys.argv) < 2 else int(sys.argv[1])

print('Iniciando sensor...')
group_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
group_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
group_socket.bind((GROUP_HOST, GROUP_PORT))
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

print('Conectando ao gateway...')
response_discover = proto.Discover()
response_discover.device_type = 'LAMP_ACTUATOR'
response_discover.communication_type = 'ACTUATOR'
response_discover.ip = HOST
response_discover.port = PORT

response = proto.Message()
response.type = 'DISCOVER'
response.discover.CopyFrom(response_discover)

sensor_socket.connect((discover_message.ip, discover_message.port))
sensor_socket.send(response.SerializeToString())

lamp_state = False

while True:
    message = proto.Message()
    message.ParseFromString(sensor_socket.recv(1024))
    print('Mensagem recebida')
    if message.type == 'COMMAND':
        command = message.command.command
        message = proto.Message(type = 'COMMAND_RESPONSE')
        if command == 'CHANGE_STATE':
            lamp_state = not lamp_state
            message.command_response.CopyFrom(proto.CommandResponse(status=True, message='STATE CHANGED'))
        if command == 'GET_STATE':
            message.command_response.CopyFrom(proto.CommandResponse(status=True, message=str('TURNED ON' if lamp_state else 'TURNED OFF')))
        if command == 'HELP':
            help_message = '\nCOMMAND: GET_STATE\nARGUMENTS: NO_ARGUMENTS\nCOMMAND: CHANGE_STATE\nARGUMENTS: NO_ARGUMENTS'
            message.command_response.CopyFrom(proto.CommandResponse(status=True, message=help_message))
        sensor_socket.send(message.SerializeToString())
