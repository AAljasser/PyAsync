import socket, threading

class sServer():
    _mainSocket = None
    _port = 8096
    _localAdd = '127.0.0.1'
    lastRecieved = None

    def __init__(self):
        if self._mainSocket is None:
            #Creating socket using ipv4 and TCP
            self._mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ## This is added for the future upgrade to multithreaded server
            self._mainSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ##Binding the server to be the main reciever of requests
            self._mainSocket.bind((self._localAdd,self._port))
        ## Server socket has been initilized there for we begin looping for requests
        self._mainSocket.listen()
        clientSock, clientAdd = self._mainSocket.accept()
        data = clientSock.recv(1024)
        print(data.decode())

    def close(self):
        self._mainSocket.close()

    class asyncClient(threading.Thread):
        def __init__(self):
            self=self

def main():
    sSocket = sServer()
    sSocket.close()


if __name__ == '__main__':
    main()