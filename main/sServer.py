import socket, threading
from main.IndState import IndState as iD
from main.Library import Library
import logging

'''
TCP Server
Using python's socket and multi-threading (threading) concurrent communication and processing of data occurs in this class
'''
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



            logging.info("Client #"+str(self._savedID)+" Sent a command")

            if dataReceived[0].casefold() == str(iD.TERMINATE_CONN):
                mToS = iD.TERMINATE_CONN
                self._mainSocket.sendall(bytes(dataReceived[0],'utf-8'))
                self._mainSocket.close()
                break
            elif self._state == iD.LOGIN: ## Check
                checking = Library().userLogin(dataReceived)
                if checking == iD.INCORRECT_INPUT: ##Inputted incorrect we cant just pass this without checking
                    mToS = str(iD.INCORRECT_INPUT)
                else:
                    self._state = checking
                    if self._state == iD.A_MENU:
                        mToS = str(checking)+','+str("Welcome to Admin menu\nCreation of staff type 'crstaff(COM)ID'")
                    elif self._state == iD.S_MENU:
                        mToS = str(checking)+','+str("Welcome to Staff menu\nCreation of patron 'crpatron(com)id(com)name'\nAddition of books  'addbook(com)id(com)title'\nto create event type 'cevent(com)eventid'\nto create lab tpye 'clab(com)labid'")
                    elif self._state == iD.P_MENU:
                        self._savedID = dataReceived[1]
                        mToS = str(checking)+','+str("Welcome to Patron menu\nTo list books tpye 'borrow'\nTo borrow a book into checkout cart type 'borrow(COM)bookcode'\nTo list current borrowed books type 'return'\nTo return borrowed books type 'return(com)bid'\nAfter borrowing book you must type checkout to obtain the books\nTo list events type 'event'\nTo register for an event type 'event(COM)eventID(COM)OPTINAL:Book id to borrow'\n to list labs type 'labs' to join a lab type 'lab(com)labID'")
            elif self._state == iD.A_MENU and 'crstaff' in dataReceived[0]:
                #Check if the Identifier doesnt already exists
                if not Library().staffExists(dataReceived[1]):
                    Library().createStaff(dataReceived[1])
                    mToS = str(self._state) + ','+'Staff creation completed'
                else:
                    mToS = str(iD.DUPLICATE_ERR) +','+'Duplicate error enter different ID'

            elif self._state == iD.S_MENU and 'cevent' in dataReceived[0]:
                if len(dataReceived) < 2:
                    mToS = str(iD.INCORRECT_INPUT)+", Please type the event ID"
                else:
                    Library().createEvent(dataReceived[1])
                    mToS = str(iD.S_MENU) + ', Event created'
            elif self._state == iD.S_MENU and 'crpatron' in dataReceived[0]:
                logging.info("Creation of Patron is begun")
                if len(dataReceived) < 3:
                    logging.info("Client entered incorrect format")
                    mToS = str(iD.INCORRECT_INPUT)
                elif not Library().patronExists(dataReceived[1]):
                    logging.info("Patron added")
                    Library().createPatron(dataReceived[1],dataReceived[2])
                    mToS =  str(self._state) + ','+'Patron creation completed'
                else:
                    logging.info("duplication")
                    mToS = str(iD.DUPLICATE_ERR) +','+'Duplicate error enter different ID'

            elif self._state == iD.S_MENU and 'addbook' in dataReceived[0]:
                logging.info("Insertion of book has begun")
                if len(dataReceived) < 3:
                    mToS = str(iD.INCORRECT_INPUT)
                    logging.info("Client entered incorrect format")
                elif not Library().bookExists(dataReceived[1]):
                    logging.info("Book added")
                    Library().addBook(dataReceived[1],dataReceived[2])
                    mToS =  str(self._state) + ','+'Book insertion completed'
                else:
                    logging.info("Duplication")
                    mToS = str(iD.DUPLICATE_ERR) +','+'Duplicate error enter different ID'
            elif self._state == iD.P_MENU and 'borrow' in dataReceived[0]:
                logging.info("Client #"+str(self._savedID)+" Sent a borrow command")
                if len(dataReceived) < 2:
                    mToS = str(self._state) +','+ Library().printBooks()
                else:
                    logging.info("Client #"+str(self._savedID)+" Sent a borrowing for "+str(dataReceived[1]))
                    if Library().borrow(self._savedID,dataReceived[1]):
                        mToS = str(self._state) + ', '+str(self._savedID)+'book has been added to cart (MUST TYPE CHECKOUT)'
                    else:
                        mToS = str(iD.BOOK_NF) + ", book doesn't exists"
            elif self._state == iD.P_MENU and 'uncheck' in dataReceived[0]:
                #removing from cart
                if len(dataReceived) >= 2:
                    if Library().uncheck(self._savedID,dataReceived[1]):
                        logging.info("Client #"+str(self._savedID)+" Removed from cart Book#"+str(dataReceived[1]))
                        mToS = str(self._state) + ', '+str(self._savedID)+'Removal from cart has been successfull'
                    else:
                        logging.info("Client #"+str(self._savedID)+" Failed removed from cart Book#"+str(dataReceived[1]))
                        mToS = str(iD.INCORRECT_INPUT) + ', '+str(self._savedID)+'Failed removal from cart'
            elif self._state == iD.P_MENU and 'return' in dataReceived[0]:
                if len(dataReceived) < 2:
                    mToS = str(self._state) +','+ Library().getPatron(self._savedID).printBBooks()
                else:
                    if Library().returnBook(self._savedID,dataReceived[1]):
                        mToS = str(self._state)+ ', Book has been returned'
                    else:
                        mToS = str(iD.INCORRECT_INPUT)
            elif self._state == iD.P_MENU and  'checkout' in dataReceived[0]:
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
            elif self._state == iD.P_MENU and 'event' in dataReceived[0]:
                logging.info("Client #"+str(self._savedID)+" Has begun an event registration request")
                if len(dataReceived) < 2:
                    mToS = str(iD.P_MENU)+","+Library().listEvents()
                elif len(dataReceived) < 3 and Library().eventExists(dataReceived[1]):
                    #Registering without borrowing
                    if Library().regEvent(dataReceived[1],self._savedID):
                        logging.info("Client #"+str(self._savedID)+" Registered into Event#"+str(dataReceived[1]))
                        mToS = str(self._state)+', Registeration Completed'
                    else:
                        logging.info("Client #"+str(self._savedID)+" Failed to register into Event#"+str(dataReceived[1]))
                        mToS = str(self._state)+', Registeration Failed'
                elif len(dataReceived) < 4 and Library().eventExists(dataReceived[1]):
                    logging.info("Client #"+str(self._savedID)+" Registration with book#" + str(dataReceived[2]))
                    #Registering with borrowing
                    if Library().regEvent(dataReceived[1],self._savedID,bid=dataReceived[2]):
                        logging.info("Client #"+str(self._savedID)+" Registered into Event#"+str(dataReceived[1])+" with Book#"+str(dataReceived[2]))
                        mToS = str(self._state)+', Registeration Completed'
                    else:
                        logging.info("Client #"+str(self._savedID)+" Failed to register into Event#"+str(dataReceived[1])+" with Book#"+str(dataReceived[2]))
                        mToS = str(self._state)+', Registeration Failed'
                else:
                    mToS = str(iD.INCORRECT_INPUT)
            elif self._state == iD.S_MENU and 'clab' in dataReceived[0]:
                if not Library().labExists(dataReceived[1]):
                    Library().createLab(dataReceived[1],10) ## THIS IS SET TO DEFAULT TO 10 seconds
                    mToS = str(self._state) +", Creation completed Queue begun"
                else:
                    mToS = str(iD.DUPLICATE_ERR) + ", Duplicated lab exists"
            elif self._state == iD.P_MENU and 'lab' in dataReceived[0]:
                if len(dataReceived) < 2:
                    mToS= str(self._state) + "," +Library().printLabs()
                elif len(dataReceived) < 3 and Library().labExists(dataReceived[1]):
                    logging.info("Client #"+str(self._savedID)+" Joined queue to join Lab#"+str(dataReceived[1]))
                    if Library().joinLab(self._savedID,dataReceived[1]):
                        logging.info("Client #"+str(self._savedID)+" Successfully joined Lab#"+str(dataReceived[1]))
                        mToS = str(self._state)+", Joined successfully"
                    else:
                        logging.info("Client #"+str(self._savedID)+" Failed to join Lab#"+str(dataReceived[1]))
                        mToS = str(iD.INCORRECT_INPUT)+", Event non-existence"
                else:
                    mToS = str(iD.INCORRECT_INPUT)

            else: #Input non exist
                if self._state == iD.LOGIN:
                    mToS = str(self._state)+", Welcome please Enter 'patron/staff(com) your ID':"
                elif self._state == iD.A_MENU:
                    mToS = str(checking)+','+str("Creation of staff type 'crstaff(COM)ID'")
                elif self._state == iD.S_MENU:
                    mToS = str(checking)+','+str("Creation of patron 'crpatron(com)id(com)name'\nAddition of books  'addbook(com)id(com)title'\nto create event type 'cevent(com)eventid'\nto create lab tpye 'clab(com)labid")
                elif self._state == iD.P_MENU:
                    mToS = str(checking)+','+str("To list books tpye 'borrow'\nTo borrow a book into checkout cart type 'borrow(COM)bookcode'\nTo list current borrowed books type 'return'\nTo return borrowed books type 'return(com)bid'\nAfter borrowing book you must type checkout to obtain the books\nTo list events type 'event'\nTo register for an event type 'event(COM)eventID(COM)OPTINAL:Book id'\n to list labs type 'labs' to join a lab type 'lab(com)labID'")
                else:
                    mToS = str(iD.TERMINATE_CONN) + ", Weird problem"

            logging.info("Client #"+str(self._savedID)+" Completed request")
            self._mainSocket.sendall(bytes(mToS,'utf-8'))
        print("Client : "+str(self._clientAdd)+" closing com, Thread_ID: "+str(threading.get_ident()))
        self._mainSocket.close()



def main():
    sSocket = sServer()
    sSocket.close()


if __name__ == '__main__':
    main()