import socket
from main.IndState import IndState as iD


'''
TCP Client
Using python's socket library communication and displaying of data for a single user
'''
class sClient():
    _mainSocket = None
    _port = 8096
    _localAdd = '127.0.0.1'
    _previousRes = None

    def __init__(self):
        self=self

    def sendO(self,msg):
        if self._mainSocket is not None:
            self._mainSocket.sendall(bytes(msg, 'UTF-8'))
        else:
            self._mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._mainSocket.connect((self._localAdd, self._port))
            self._mainSocket.sendall(bytes(msg, 'UTF-8'))

    def send(self, msg):
        if self._mainSocket is not None:
            self._mainSocket.sendall(bytes(msg, 'UTF-8'))
            data = self._mainSocket.recv(2048)
            recMsg = data.decode('utf-8').casefold()

            return iD.breakData(recMsg)
        else:
            self._mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._mainSocket.connect((self._localAdd, self._port))
            self._mainSocket.sendall(bytes(msg, 'UTF-8'))
            data = self._mainSocket.recv(2048)
            recMsg = data.decode('utf-8').casefold()

            return iD.breakData(recMsg)

    def close(self):
        self._mainSocket.close()

    def lastRes(self):
        return self._previousRes

    def terminal(self):
        print("Welcome please Enter 'patron/staff, your ID':")
        toBeSent = str(input()).replace(" ", "")
        receivedMessage = self.send(toBeSent)
        # If Terminate is recieved we exit the loop and close socket
        while receivedMessage[0] != str(iD.TERMINATE_CONN):
            if receivedMessage[0] == str(iD.INCORRECT_INPUT):
                print("Incorrect input, please ensure you include a comma (,)")
            elif receivedMessage[0] == str(iD.DUPLICATE_ERR):
                print("Duplicate input")
            #Check status and print accordingly
            #Checking what has been received
            for x in range(1,len(receivedMessage)):
                print(receivedMessage[x])

            toBeSent = str(input()).replace(" ", "")

            if toBeSent.casefold() == 'exit' or toBeSent.casefold() == 'logout' or toBeSent.casefold() == 'off':
                self.send(str(iD.TERMINATE_CONN))
                break

            receivedMessage = self.send(toBeSent)
            #Checking what has been received

        #Closing
        self.close()

def main():
    s = sClient()
    s.terminal()

if __name__ == '__main__':
    main()