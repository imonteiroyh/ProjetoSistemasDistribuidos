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

            if data.split()[0] == '/ENTRAR':
                if nicknames[connection_socket] == 'generic_username':
                    try:
                        nicknames[connection_socket] = data.split()[1]
                        for connection in connections:
                            in_message = nicknames[connection_socket] + ' entrou na sala.'
                            if connection != connection_socket:
                                connection.send(in_message.encode('utf-8'))
                    except:
                        error = 'Comando válido: /ENTRAR nickname'
                        connection_socket.send(error.encode('utf-8'))
                else:
                    error = 'Comando inválido. Usuário já entrou na sala.'
                    connection_socket.send(error.encode('utf-8'))

            elif data.split()[0] == '/USUARIOS':
                
            elif data.split()[0] == '/SAIR':

            else:



        except:
            break

    print('Conexão encerrada.')

    try:
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

    start_new_thread(threaded_client, (connection_socket))
