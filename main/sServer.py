import socket, threading

class sServer():
    _mainSocket = None
    _port = 8096
    _localAdd = '127.0.0.1'
    _connected = []

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
        while True:
            clientSock, clientAdd = self._mainSocket.accept()
            print("Client : "+str(clientAdd)+" has connected")
            self._connected.append(asyncClient(clientSock,clientAdd))

    def close(self):
        self._mainSocket.close()

class asyncClient(threading.Thread, sServer):
    _clientAdd = None
    def __init__(self, socket, clintAdd):
        self._mainSocket = socket
        self._clientAdd = clintAdd



def main():
    sSocket = sServer()
    sSocket.close()


if __name__ == '__main__':
    main()