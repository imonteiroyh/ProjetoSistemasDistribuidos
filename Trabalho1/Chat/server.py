import socket
from _thread import *

server = '127.0.0.1'
port = 9898

# Criando o soquete servidor utilizando IPv4 e TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((server, port))
except socket.error as error:
    print(error)

# Habilitando o servidor para aceitar conexões
server_socket.listen()
print('Servidor iniciado. Esperando conexões...')

connections = []
nicknames = {}

def threaded_client(connection_socket):

    while True:
        try:
            data = connection_socket.recv(2048).decode()

            if data == '':
                continue

            elif data.split()[0] == '/ENTRAR':
                if nicknames[connection_socket] == 'generic_username':
                    try:
                        nicknames[connection_socket] = data.split()[1]
                        for connection in connections:
                            in_message = 'Servidor: ' + nicknames[connection_socket] + ' entrou na sala.'
                            if connection != connection_socket:
                                connection.send(in_message.encode('utf-8'))
                    except:
                        error = 'Comando válido: /ENTRAR nickname'
                        connection_socket.send(error.encode('utf-8'))
                else:
                    error = 'Comando inválido. Usuário já entrou na sala.'
                    connection_socket.send(error.encode('utf-8'))

            elif data.split()[0] == '/USUARIOS':
                if nicknames[connection_socket] != 'generic_username':
                    for _, nickname in nicknames.items():
                        if nickname != 'generic_username':
                            connection_socket.send(nickname.encode('utf-8'))
                else:
                    error = 'Comando inválido. Usuário precisa entrar na sala antes de usar esse comando.'
                    connection_socket.send(error.encode('utf-8'))

            elif data.split()[0] == '/SAIR':
                end_message = 'encerrar'
                connection_socket.send(end_message.encode('utf-8'))
                break

            else:
                if nicknames[connection_socket] != 'generic_username':
                    for connection in connections:
                        if connection != connection_socket and nicknames[connection] != 'generic_username':
                            data = f'{nicknames[connection_socket]}: ' + data
                            connection.send(data.encode('utf-8'))
                else:
                    error = 'Usuário precisa entrar na sala para enviar mensagens.'
                    connection_socket.send(error.encode('utf-8'))

        except:
            break

    print('Conexão encerrada.')

    try:
        del nicknames[connection_socket]
        connections.remove(connection_socket)
    except:
        pass

    connection_socket.close()

# Servidor aberto, aceitando conexões
while True:
    connection_socket, address = server_socket.accept()
    print('Conectado a: ', address)

    connections.append(connection_socket)
    nicknames[connection_socket] = 'generic_username'

    start_new_thread(threaded_client, (connection_socket, ))