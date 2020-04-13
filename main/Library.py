from main.IndState import IndState as iD
from main.Patron import Patron
from main.Book import Book
import logging


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
    lock = None



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
        logging.info("Patron #"+str(pid)+": Trying to borrow "+str(bid))
        if self.bookExists(bid):
            if not self.getPatron(pid).bExists(bid):
                self.getPatron(pid).addBook(bid,self.getBook(bid))
                del self._book[bid]
                logging.info("Patron #"+str(pid)+": Successful to borrow "+str(bid))
                return True
        logging.info("Patron #"+str(pid)+": Failed to borrow "+str(bid))
        return False
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
