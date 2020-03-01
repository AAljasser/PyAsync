from IndState import IndState as iD
from main.Patreon import Patreon
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
    #Patreons users and passwords stored
    instance = None
    _patreon = {'p1000':Patreon('p1000','abdul'),'p1001':Patreon('p1001','PatreonOne'),'p1002':Patreon('p1002','PatreonTwo')}
    _staff = ['s1000']
    _book = {'b1000':Book('b1000','HungerGames'),'b1001':Book('b1001','Game of Thrones'),'b1002':Book('b1002','Lord of the Flies')}
    _admin = 'admin'



    def userLogin(self,info):
        name = None
        oIfo = None
        if len(info) > 1:
            name = info[0]
            oIfo = info[1]
        else:
            name = info[0]
        #logging.basicConfig(filename='logs/library.log',level=logging.INFO)
        logging.info(str(name)+": Trying to log in")
        if name.casefold() == 'admin':
            logging.info(str(name)+": Admin log in successful")
            return iD.A_MENU
        elif name.casefold() == 'staff':
            if self.staffExists(oIfo):
                logging.info(str(name)+": Staff log in successful")
                return iD.S_MENU
            else:
                return iD.INCORRECT_INPUT
        elif name.casefold() == 'patreon':
            if self.patreonExists(oIfo):
                logging.info(str(name)+": Patreon log in successful")
                return iD.P_MENU
            else:
                return iD.INCORRECT_INPUT
        else:
            return iD.INCORRECT_INPUT

    def createStaff(self,id):
        self._staff.append(id.casefold())
    def createPatreon(self, id, name):
        self._patreon[id]=Patreon(name,id)
    def patreonExists(self,id):
        return id.casefold() in self._patreon.keys()
    def getPatreon(self,id):
        if self.patreonExists(id):
            return self._patreon[id]
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
        #logging.basicConfig(filename='logs/library.log',level=logging.INFO)
        logging.info(str(pid)+" Patreon: Trying to borrow "+str(bid))
        print("HERHERHEREHRHERER")
        print(self.bookExists(bid))
        if self.bookExists(bid):
            if not self.getPatreon(pid).bExists(bid): #Book hasnt been borrowed, or no duplicate exists
                self.getPatreon(pid).addBook(bid,self.getBook(bid))
                del self._book[bid]
                logging.info(str(pid)+" Patreon: Successful to borrow "+str(bid))
                return True
        logging.info(str(pid)+" Patreon: Failed to borrow "+str(bid))
        return False
    def returnBook(self,pid,bid):
        print(pid,bid)
        if self.getPatreon(pid).bExists(bid):
            self._book[bid] = self.getPatreon(pid).removeBook(bid)
            return True
        else:
            return False
    def printBooks(self):
        retMsg = ''
        for x in self._book.keys():
            retMsg = retMsg + x + ": "+self._book[x].get_title()+','
        return retMsg