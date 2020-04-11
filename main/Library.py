from main.IndState import IndState as iD
from main.Patron import Patron
from main.Book import Book
from main.Event import Event
import logging
import threading
from main.Lab import Lab


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Library(metaclass=Singleton):
    pass
    #Patrons users and passwords stored
    instance = None
    _patron = {'p1000':Patron('p1000','abdul'),'p1001':Patron('p1001','PatronOne'),'p1002':Patron('p1002','PatronTwo')}
    _staff = ['s1000']
    _book = {'b1000':Book('b1000','HungerGames'),'b1001':Book('b1001','Game of Thrones'),'b1002':Book('b1002','Lord of the Flies')}
    _admin = 'admin'
    _checkOut = {} #This will contain as a key (BOOK ID) and the value is the (PATRON ID) holding book
    lock = None
    _events = {'e1001':Event('e1001','Book Reading Event')} #Will contain an ID as key and LIST of users in the event
    _labs = {'l2000':Lab('l2000',1),'l3000':Lab('l3000',1)} #Contains labs object and key is the labs ID


    def userLogin(self,info):
        name = None
        oIfo = None
        if len(info) > 1:
            name = info[0]
            oIfo = info[1]
        else:
            name = info[0]
        logging.info(str(name)+": Trying to log in")
        if name.casefold() == 'admin':
            logging.info(str(name)+": Admin log in successful")
            return iD.A_MENU
        elif name.casefold() == 'staff':
            if self.staffExists(oIfo):
                logging.info("Staff #"+str(name)+": log in successful")
                return iD.S_MENU
            else:
                return iD.INCORRECT_INPUT
        elif name.casefold() == 'patron':
            if self.patronExists(oIfo):
                logging.info("Patron #"+str(name)+":log in successful")
                return iD.P_MENU
            else:
                return iD.INCORRECT_INPUT
        else:
            return iD.INCORRECT_INPUT

    def createStaff(self,id):
        self._staff.append(id.casefold())
    def createPatron(self, id, name):
        self._patron[id]=Patron(name,id)
    def patronExists(self,id):
        return id.casefold() in self._patron.keys()
    def getPatron(self,id):
        if self.patronExists(id):
            return self._patron[id]
    def getBook(self,id):
        if self.bookExists(id):
            return self._book[id]
    def staffExists(self,id):
        return id.casefold() in self._staff
    def bookExists(self,id):
        return id.casefold() in self._book.keys()
    def addBook(self,id,title):
        self._book[id] = Book(title,id)

    def borrow(self,pid,bid):
        #TODO: must implement holding of lock
        ##Know book object contains a lock and has an aquire and release functions
        if self.bookExists(bid):
            logging.info("Patron #"+str(pid)+": Trying to acquire lock of book "+str(bid))
            #JUMPING A CHECK IF THE BOOK EXISTS IN THE PATRON ALREADY
            if self.getBook(bid).checkLock():
                logging.info("Patron #"+str(pid)+": Failed to acquire lock "+str(bid))
                return False
            self.getBook(bid).acqLock() ## HERE WE ACQUIRE THE LOCK FOR THE BOOK that will be added for the patrons checkout
            if self.checked(bid):
                return False
            self._checkOut[bid]=pid
            threading.Timer(30,Library().uncheck,[pid,bid]).start()
            logging.info("Patron #"+str(pid)+": Successful to acquire lock of book "+str(bid))
            #TODO: Setup timer to remove lock and book from checkout
            return True
        return False

    def uncheck(self,pid,bid):
        if bid in self._checkOut.keys():
            if pid in self._checkOut[bid]:
                del self._checkOut[bid]
                self.getBook(bid).relLock()
                logging.info("Patron #"+str(pid)+": Removed from cart Book#"+str(bid))
                return True
        logging.info("Patron #"+str(pid)+": Failed to Removed from cart Book#"+str(bid))
        return False
        #logging.basicConfig(filename='logs/library.log',level=logging.INFO)
        # logging.info("Patron #"+str(pid)+": Trying to borrow "+str(bid))
        # if self.bookExists(bid):
        #     if not self.getPatron(pid).bExists(bid): #Book hasnt been borrowed, or no duplicate exists
        #         self.getPatron(pid).addBook(bid,self.getBook(bid))
        #         del self._book[bid]
        #         logging.info("Patron #"+str(pid)+": Successful to borrow "+str(bid))
        #         return True
        # logging.info("Patron #"+str(pid)+": Failed to borrow "+str(bid))
        # return False
    def returnBook(self,pid,bid):
        if self.getPatron(pid).bExists(bid):
            self._book[bid] = self.getPatron(pid).removeBook(bid)
            return True
        else:
            return False
    def printBooks(self):
        retMsg = ''
        for x in self._book.keys():
            retMsg = retMsg + x + ": "+self._book[x].get_title()+','
        return retMsg

    def checked(self,bid):
        if bid in self._checkOut.keys():
            return True
        else:
            return False

    def printCheckOut(self,id):
        ret = "Cart Contains\n"
        for x in self._checkOut:
            if self._checkOut[x] in id: #checking which user has which book
                ret = ret + "Book ID: "+x+", Title: "+self.getBook(x).get_title()
                ret = ret + '\n'
        return ret

    def checkOut(self,id):# NO return
        flag = False
        logging.info("Patron #"+str(id)+": Trying to checkout ")
        toRemove = []
        for x in self._checkOut:
            if self._checkOut[x] in id: #checking which user has which book
                flag = True
                self.getPatron(self._checkOut[x]).addBook(x,self.getBook(x))
                logging.info("Patron #"+str(id)+": Trying to checkout "+str(x))
                self.getPatron(self._checkOut[x]).getBook(x).relLock()
                logging.info("Patron #"+str(id)+": Released "+str(x))
                toRemove.append(x)
                del self._book[x]
        for x in toRemove:
            del self._checkOut[x]
        return flag

        #The checkout supposed to do what the previous borrow function does

        # if self.bookExists(bid):
        #     if not self.getPatron(pid).bExists(bid): #Book hasnt been borrowed, or no duplicate exists
        #         self.getPatron(pid).addBook(bid,self.getBook(bid))
        #         del self._book[bid]
        #         logging.info("Patron #"+str(pid)+": Successful to borrow "+str(bid))
        #         return True
        # logging.info("Patron #"+str(pid)+": Failed to borrow "+str(bid))
        # return False


    def listEvents(self):
        ret = "Reading events available\n"
        for x in self._events.keys():
            ret = ret + "Event ID: "+x
            ret = ret + '\n'
        return ret

    def createEvent(self,id):
        if id not in self._events.keys():
            self._events[id] = Event(id,"Book Event") #No title currently can be added
    def eventExists(self,id):
        if id in self._events.keys():
            return True
        else:
            return False
    def regEvent(self,id,pid,bid=None):
        #We begin by acquiring event LOCK
        if not self.eventExists(id):
            return False
        logging.info("Patron #"+str(pid)+" Acquiring Lock of Event "+str(id))
        self._events[id].acqL()

        if bid is None:
            logging.info("Patron #"+str(pid)+" Registering in Event "+str(id)+" As brining their own Book")
        else:
            logging.info("Patron #"+str(pid)+" Registering in Event "+str(id)+" Requesting Book ID#"+str(bid))
            flag = self.borrow(pid,bid)
            if not flag:
                logging.info("Patron #"+str(pid)+" Failed to get book for register")
                self._events[id].reL()
                return False
            self.checkOut(pid)
            logging.info("Patron #"+str(pid)+" Registering in Event "+str(id)+" Completed Borrowing Book ID#"+str(bid))
        self.getPatron(pid).regIn(id)
        self._events[id].register(pid)
        self._events[id].reL()
        logging.info("Patron #"+str(pid)+" Completed Registering in Event "+str(id))
        return True

    def createLab(self,labID,timeToOpen):
        if labID not in self._labs.keys():
            self._labs[labID] = Lab(labID,timeToOpen)

    def labExists(self,labID):
        if labID in self._labs.keys():
            return True
        else:
            return False

    def joinLab(self,pid,lid):
        if self.labExists(lid):
            return self._labs[lid].join(pid)
        else:
            return False #Nonexistence lab

    def getLab(self,lid):
        if self.labExists(lid):
            return self._labs[lid]

    def printLabs(self):
        pL = "Labs available: "
        for x in self._labs.keys():
            pL = pL + "\nLab #:"+str(x)
        return pL