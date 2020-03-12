import socket, threading
from IndState import IndState as iD
from main.Library import Library
import logging

class sServer():
    _mainSocket = None
    _port = 8096
    _localAdd = '127.0.0.1'
    _connected = []
    _cond = threading.Condition()
    def __init__(self):
        Library()
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
            x = asyncClient(clientSock,clientAdd)

            self._connected.append(x)
            x.start()

    def close(self):
        self._mainSocket.close()

##MULTI THREADED Communication line to client
class asyncClient(threading.Thread, sServer):
    _clientAdd = None
    _previousRes = None #This is used to keep previous responses, to reduce data sent between server and client
    _state = iD.LOGIN #All connected clients are in login mode
    _savedID = None

    def __init__(self, socket, clintAdd):
        threading.Thread.__init__(self)

        self._mainSocket = socket
        self._clientAdd = clintAdd

    def run(self):
        print("Client : "+str(self._clientAdd)+" has connected, Thread_ID: "+str(threading.get_ident()))
        mToS = None # Messageto be sent to the client
        while mToS != iD.TERMINATE_CONN:
            logging.warning("Client #"+str(self._savedID)+" Waiting for message")
            receivedMsg = self._mainSocket.recv(2048)

            dataReceived = iD.breakData(receivedMsg.decode('utf-8')) ##Server/Client always commun



            logging.info("Client #"+str(self._savedID)+"Sent a command")
            print(dataReceived)

            if dataReceived[0].casefold() == str(iD.TERMINATE_CONN):
                mToS = iD.TERMINATE_CONN
                self._mainSocket.sendall(bytes(dataReceived[0],'utf-8'))
                self._mainSocket.close()
                break
            elif self._state == iD.LOGIN: ## Check
                #TODO
                checking = Library().userLogin(dataReceived)
                if checking == iD.INCORRECT_INPUT: ##Inputted incorrect we cant just pass this without checking
                    mToS = str(iD.INCORRECT_INPUT)
                else:
                    self._state = checking
                    if self._state == iD.A_MENU:
                        mToS = str(checking)+','+str("Welcome to Admin menu\nCreation of staff type 'crstaff(COM)ID'")
                    elif self._state == iD.S_MENU:
                        mToS = str(checking)+','+str("Welcome to Staff menu\nCreation of patreon 'crpatreon(com)id(com)name'\nAddition of books  'addbook(com)id(com)title'")
                    elif self._state == iD.P_MENU:
                        self._savedID = dataReceived[1]
                        mToS = str(checking)+','+str("Welcome to Patreon menu\nTo list books tpye 'borrow'\nTo borrow a book into checkout cart type 'borrow(COM)bookcode'\nTo list current borrowed books type 'return'\nTo return borrowed books type 'return(com)bid'\nAfter borrowing book you must type checkout to obtain the books")
            elif self._state == iD.A_MENU and dataReceived[0] == 'crstaff':
                #Check if the Identifier doesnt already exists
                if not Library().staffExists(dataReceived[1]):
                    Library().createStaff(dataReceived[1])
                    mToS = str(self._state) + ','+'Staff creation completed'
                else:
                    mToS = str(iD.DUPLICATE_ERR) +','+'Duplicate error enter different ID'
            elif self._state == iD.S_MENU and dataReceived[0] == 'crpatreon':
                print("Creation of Patreaon is begun")
                if len(dataReceived) < 3:
                    print("Client entered incorrect format")
                    mToS = str(iD.INCORRECT_INPUT)
                elif not Library().patreonExists(dataReceived[1]):
                    print("Patreon added")
                    Library().createPatreon(dataReceived[1],dataReceived[2])
                    mToS =  str(self._state) + ','+'Patreon creation completed'
                else:
                    print("duplication")
                    mToS = str(iD.DUPLICATE_ERR) +','+'Duplicate error enter different ID'

            elif self._state == iD.S_MENU and dataReceived[0] == 'addbook':
                print("Insertion of book has begun")
                if len(dataReceived) < 3:
                    mToS = str(iD.INCORRECT_INPUT)
                    print("Client entered incorrect format")
                elif not Library().bookExists(dataReceived[1]):
                    print("Book added")
                    Library().addBook(dataReceived[1],dataReceived[2])
                    mToS =  str(self._state) + ','+'Book insertion completed'
                else:
                    print("Duplication")
                    mToS = str(iD.DUPLICATE_ERR) +','+'Duplicate error enter different ID'
            elif self._state == iD.P_MENU and dataReceived[0] == 'borrow':
                logging.info("Client #"+str(self._savedID)+"Sent a borrow command")
                if len(dataReceived) < 2:
                    mToS = str(self._state) +','+ Library().printBooks()
                else:
                    logging.info("Client #"+str(self._savedID)+"Sent a borrowing for "+str(dataReceived[1]))
                    if Library().borrow(self._savedID,dataReceived[1]):
                        mToS = str(self._state) + ', '+str(self._savedID)+'book has been added to cart (MUST TYPE CHECKOUT)'
                    else:
                        mToS = str(iD.BOOK_NF) + ", book doesn't exists"
            elif self._state == iD.P_MENU and dataReceived[0] == 'return':
                if len(dataReceived) < 2:
                    mToS = str(self._state) +','+ Library().getPatreon(self._savedID).printBBooks()
                else:
                    if Library().returnBook(self._savedID,dataReceived[1]):
                        mToS = str(self._state)+ ', Book has been returned'
                    else:
                        mToS = str(iD.INCORRECT_INPUT)
            elif self._state == iD.P_MENU and dataReceived[0] == 'checkout':
                #If user provide parameters with checkout we must proceed accordingly
                if len(dataReceived) < 2: #No parameters
                    #Here we checkout the users cart
                    mToS = str(self._state)+','+Library().printCheckOut(self._savedID)
                    if Library().checkOut(self._savedID):
                        mToS = mToS+', The printed books have been checked out'
                    else:
                        mToS = str(self._state)+', No books in cart to be checkedout'
                elif len(dataReceived) >= 2 and ("view" in dataReceived[1]):
                    #Here we view what the users checkout contains
                    mToS = str(self._state)+','+Library().printCheckOut(self._savedID)
                else:
                    mToS = str(iD.INCORRECT_INPUT)
            else: #Input non exist
                if self._state == iD.LOGIN:
                    mToS = str(self._state)+"Welcome please Enter 'patreon/staff(com) your ID':"
                elif self._state == iD.A_MENU:
                    mToS = str(checking)+','+str("Creation of staff type 'crstaff(COM)ID'")
                elif self._state == iD.S_MENU:
                    mToS = str(checking)+','+str("Creation of patreon 'crpatreon(com)id(com)name'\nAddition of books  'addbook(com)id(com)title'")
                elif self._state == iD.P_MENU:
                    mToS = str(checking)+','+str("To list books tpye 'borrow'\nTo borrow a book into checkout cart type 'borrow(COM)bookcode'\nTo list current borrowed books type 'return'\nTo return borrowed books type 'return(com)bid'\nAfter borrowing book you must type checkout to obtain the books")
                else:
                    mToS = str(iD.TERMINATE_CONN) + "Weird problem"

            print(mToS)
            logging.info("Client #"+str(self._savedID)+"Completed request")
            self._mainSocket.sendall(bytes(mToS,'utf-8'))
        print("Client : "+str(self._clientAdd)+" closing com, Thread_ID: "+str(threading.get_ident()))
        self._mainSocket.close()



def main():
    logging.basicConfig(filename='library.log',level=logging.INFO)
    sSocket = sServer()
    sSocket.close()


if __name__ == '__main__':
    main()