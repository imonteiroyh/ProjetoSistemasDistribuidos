import socket
import traceback
import _thread

serverAddr = '127.0.0.1'
serverPort = 9898

try:
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientSocket.connect((serverAddr, serverPort))
except Exception:
    print(traceback.format_exc())

run = True

def sendMessage(Socket):
    global run

    while run:
        data = input()
        data = data.encode('utf-8')
        try:
            Socket.send(data)
        except Exception:
            print(traceback.format_exc())


def recMessage(Socket):
    global run

    while run:
        try:
            mensagem = Socket.recv(3096)
            mensagem = mensagem.decode('utf-8')
            if mensagem == 'encerrar':
                print('Usuário desconectado.')
                run = False
                break
            print(mensagem)

        except Exception:
            print(traceback.format_exc())


_thread.start_new_thread(sendMessage, (clientSocket,))
_thread.start_new_thread(recMessage, (clientSocket,))

while True:
    if run:
        pass
    else:
        raise SystemExit