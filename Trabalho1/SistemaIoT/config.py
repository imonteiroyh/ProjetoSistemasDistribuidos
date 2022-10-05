import socket
from contextlib import closing

GROUP_HOST = '228.0.0.7'
GROUP_PORT = 19000

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as _socket:
        _socket.bind(('', 0))
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return _socket.getsockname()[1]