import socket

class sClient():
    _mainSocket = None
    _port = 8096
    _localAdd = '127.0.0.1'

    def __init__(self):
        if self._mainSocket is None:
            #Creating socket using ipv4 and TCP
            self._mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._mainSocket.connect((self._localAdd, self._port))

    def send(self, msg):
        if self._mainSocket is not None:
            self._mainSocket.sendall(bytes(msg, 'UTF-8'))

    def close(self):
        self._mainSocket.close()