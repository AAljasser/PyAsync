from IndState import IndState as iD
from main.Patreon import Patreon
from main.Book import Book

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
    _patreon = {'p1000':Patreon('p1000','abdul')}
    _staff = ['s1000']
    _book = {'b1000':Book('b1000','HungerGames')}
    _admin = 'admin'


    def userLogin(self,info):
        name = None
        oIfo = None
        if len(info) > 1:
            name = info[0]
            oIfo = info[1]
        else:
            name = info[0]
        if name.casefold() == 'admin':
            return iD.A_MENU
        elif name.casefold() == 'staff':
            if self.staffExists(oIfo):
                return iD.S_MENU
            else:
                return iD.INCORRECT_INPUT
        elif name.casefold() == 'patreon':
            return iD.P_MENU
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
        if self.bookExists(bid):
            if not self.getPatreon(pid).bExists(bid): #Book hasnt been borrowed, or no duplicate exists
                self.getPatreon(pid).addBook(bid,self.getBook(bid))
                del self._book[bid]
                return True
        return False