from main.IndState import IndState as iD
from main.Patron import Patron
from main.Book import Book
from main.Event import Event
import logging
import threading
from main.Lab import Lab

'''
Class that instructs Python if a class has it's metaclass set to Singleton to return the same object of Library
Allows usage of 
    "Library()"
    "Library().exampleFunction()"
And the data will be globally shared (Singleton). This practice is used to ease induction of non-deterministic behaviors.
'''
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

'''
Class: Library (Singleton)
Attributes:
    _patron: Dictionary containing Patron's ID as key mapped to Patron Class Object
    _staff: List of staff IDs
    _patron: Dictionary containing Book's ID as key mapped to Book Class Object
    _events: Dictionary containing Event's ID as key mapped to Event Class Object
    _labs: Dictionary containing Lab's ID as key mapped to Lab Class Object
    lock: (UNUSED) Removed since Deadlock
    _checkOut: Checkout map of patron's ID and book's ID
'''
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


    '''
    Function associated with confirming credentials to access the system
        Boolean return: Granting access
    '''
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
                logging.error(str(name)+": FAILED LOGIN - INVALID ID provided")
                return iD.INCORRECT_INPUT
        elif name.casefold() == 'patron':
            if self.patronExists(oIfo):
                logging.info("Patron #"+str(name)+":log in successful")
                return iD.P_MENU
            else:
                logging.error(str(name)+": FAILED LOGIN - INVALID ID provided")
                return iD.INCORRECT_INPUT
        else:
            logging.error(str(name)+": FAILED LOGIN - INVALID ID provided")
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

    '''
    Transitioned function (Functions as adding to checkout cart)
    A thread safe function that allows patron to append their book into _checkout dictionary
    execution of checkout function will transition the book outside of the library and into the patron's book collections
    '''
    def borrow(self,pid,bid):
        '''
        :param pid: Patron ID
        :param bid: Book ID
        :return: True if book has been successfully added into _checkOut, else False
        '''
        if self.bookExists(bid):
            logging.info("Patron #"+str(pid)+": Trying to acquire lock of book "+str(bid))
            '''
            Diverting from forever waiting for a locked book (In library but in someone else's cart) adding to cart returns false if book is not available
            '''
            if self.getBook(bid).checkLock():
                logging.info("Patron #"+str(pid)+": Failed to acquire lock "+str(bid))
                return False
            '''
            After checking the lock isn't being held by a checkout the current thread acquires the book's lock
            '''
            self.getBook(bid).acqLock() ## HERE WE ACQUIRE THE LOCK FOR THE BOOK that will be added for the patrons checkout
            '''
            Con-current possibility that previous check (LINE 117) returned False right after an acquired lock by another thread (Which completed adding to cart)
            Solution another check to ensure the book isn't checked (In another patron's cart) by another patron
            '''
            if self.checked(bid):
                return False
            '''
            Adding the book into checkout system, and initiating timer function that returns the book 
            into the library system and releases the lock held by the patron
            '''
            self._checkOut[bid]=pid
            threading.Timer(15,Library().uncheck,[pid,bid]).start()
            logging.info("Patron #"+str(pid)+": Successful to acquire lock of book and added to checkout"+str(bid))
            return True
        logging.info("Patron #"+str(pid)+": Book#"+str(bid)+" Doesn't exists")
        return False

    '''
    Function to remove patron's book from _checkOut dictionary and releasing associated lock
    '''
    def uncheck(self,pid,bid):
        if bid in self._checkOut.keys():
            if pid in self._checkOut[bid]:
                del self._checkOut[bid]
                self.getBook(bid).relLock()
                logging.info("Patron #"+str(pid)+": Removed from cart Book#"+str(bid))
                return True
            else:
                return False
        else:
            logging.info("Patron #"+str(pid)+": Failed to Removed from cart Book#"+str(bid))
            return False

    '''
    Book returnal to Library System
    '''
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

    '''
    Boolean function checks if the asked book is in the _checkOut dictionary
    '''
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

    '''
    Removal of book out of the library system into the associated patron found in _checkOut
    '''
    def checkOut(self,id):
        flag = False
        logging.info("Patron #"+str(id)+": Trying to checkout ")
        toRemove = []
        for x in self._checkOut:
            if self._checkOut[x] in id: #checking which user has which book
                flag = True
                self.getPatron(self._checkOut[x]).addBook(x,self.getBook(x))
                logging.info("Patron #"+str(id)+": Trying to checkout "+str(x))
                '''
                Important (Locks acquired in borrow is released here) therefore the checked (Line:125) function would returned false (and causing error dicussed in Deadlock section)
                Therefore the check (Line:114) prevent the case where a non-existing book being added in the _checkOut 
                '''
                self.getPatron(self._checkOut[x]).getBook(x).relLock()
                logging.info("Patron #"+str(id)+": Released "+str(x))
                toRemove.append(x)
                del self._book[x]
        for x in toRemove:
            del self._checkOut[x]
        return flag



    def listEvents(self):
        ret = "Reading events available\n"
        for x in self._events.keys():
            ret = ret + "Event ID: "+x
            ret = ret + '\n'
        return ret

    '''Creation of Event Object (Prevention of duplication)'''
    def createEvent(self,id):
        if id not in self._events.keys():
            self._events[id] = Event(id,"Book Event")

    def eventExists(self,id):
        if id in self._events.keys():
            return True
        else:
            return False

    def regEvent(self,id,pid,bid=None):
        '''
        Thread safe implementation of registration of library Event
        :param id: Event ID
        :param pid: Patron ID
        :param bid: (Optional) Book idea to be borrowed while registering to Event
        :return: True if successful, false otherwise (Specific reason logged)

        Implementing thread Lock for each Lab object produce thread safe function
        '''

        if not self.eventExists(id):
            return False
        logging.info("Patron #"+str(pid)+" Acquiring Lock of Event "+str(id))
        '''
        After Event is determined to exists, the lock is acquired before any manipulation to the actual even object is begun
        If lock is held by another thread, current thread invokes sleep until the lock is released
        '''
        self._events[id].acqL()

        '''
        After Sucessful lock acquiring, other checks are done before completion of the registration
        If a Book ID is provided, then therefore the library system must successfully 
        complete borrow(Adding to cart)/checkout function of the requested book
        '''
        if bid is None:
            logging.info("Patron #"+str(pid)+" Registering in Event "+str(id)+" As brining their own Book")
        else:
            logging.info("Patron #"+str(pid)+" Registering in Event "+str(id)+" Requesting Book ID#"+str(bid))
            '''Using the thread safe function Borrow we attempt to borrow the requested book'''
            flag = self.borrow(pid,bid)
            if not flag:
                '''If Book borrowing fails then the event registration also fails'''
                logging.info("Patron #"+str(pid)+" Failed to get book for register")
                self._events[id].reL()
                return False
            '''If book borrowing is successful then checkout of the book is completed to continue with the event registration'''
            self.checkOut(pid)
            logging.info("Patron #"+str(pid)+" Registering in Event "+str(id)+" Completed Borrowing Book ID#"+str(bid))
        '''After continuing the process of borrowing the optional book the patron is registered into the even'''
        self.getPatron(pid).regIn(id)
        self._events[id].register(pid)
        '''Lastly releasing events lock after concluding patron's registration'''
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
            return False

    def getLab(self,lid):
        if self.labExists(lid):
            return self._labs[lid]

    def printLabs(self):
        pL = "Labs available: "
        for x in self._labs.keys():
            pL = pL + "\nLab #:"+str(x)
        return pL