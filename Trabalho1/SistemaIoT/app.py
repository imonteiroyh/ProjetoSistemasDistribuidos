import socket
import sys, select, os
from serializers import message_pb2 as proto

HOST = 'localhost'
PORT = 7994 if len(sys.argv) < 2 else int(sys.argv[1])
GATEWAY_HOST = 'localhost'
GATEWAY_PORT = 7884

print('Iniciando aplicação...')
app_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
app_socket.bind((HOST, PORT))

app_socket.connect((GATEWAY_HOST, GATEWAY_PORT))

message = proto.Message(type='DISCOVER')
message.discover.CopyFrom(proto.Discover(device_type='APP'))

app_socket.send(message.SerializeToString())

while True:

    device_message = proto.Message()
    device_message.ParseFromString(app_socket.recv(1024))

    for device in device_message.device_list.devices:
        print()
        print(f'Dispositivo {device.id}')
        print(f'Tipo de dispositivo: {device.device_type}')
        print(f'Tipo de comunicação: {device.communication_type}')
        print()

    user_device_id = int(input('Com qual dispositivo deseja se comunicar? '))

    #print(user_device_id)

    device_type_requested = ''
    for device in device_message.device_list.devices:
        if device.id == user_device_id:
            message = proto.Message(type='DEVICE')
            message.device.CopyFrom(proto.Device(id=device.id, device_type=device.device_type, communication_type=device.communication_type))
            device_type_requested = device.communication_type
            #rint(message.device.id)
            #print(device_type_requested)
            app_socket.send(message.SerializeToString())
            break
        

    if device_type_requested == 'SENSOR':
        while True:
            message = proto.Message()
            message.ParseFromString(app_socket.recv(1024))
            print(f'Dados: {message.data.data}')
            continue_message = proto.Message()
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = input()
                continue_message.command.CopyFrom(proto.Command(command='STOP'))
                app_socket.send(continue_message.SerializeToString())
                break
            continue_message.command.CopyFrom(proto.Command(command='CONTINUE'))
            app_socket.send(continue_message.SerializeToString())

    else:
        user_command = input('Digite o comando que deseja enviar para o atuador: ')
        user_arguments = input('Digite os argumentos: ').split(' ')
        message = proto.Message(type='COMMAND')
        message.command.CopyFrom(proto.Command(command=user_command, arguments=user_arguments))
        app_socket.send(message.SerializeToString())
        message = proto.Message()
        message.ParseFromString(app_socket.recv(1024))
        print()
        print(f'Status: {message.commandResponse.status}')
        print(f'Mensagem: {message.commandResponse.message}')