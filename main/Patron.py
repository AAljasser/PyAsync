
'''
Class: Patron
Attributes:
    pid: Patron ID
    pname: Patron Name
    bCollection: Book collection
    eventR: Events resgistered
'''
class Patron():
    _pid = None
    _pname = None
    _bCollection = None
    _eventR = None
    def __init__(self,name,id):
        self._pname = name
        self._pid = id
        self._bCollection = {}
        self._eventR = [] #
    def get_id(self):
        return self._pid
    def get_name(self):
        return self._pname
    def addBook(self,bid,bobj):
        if self._bCollection is not None:
            if bid not in self._bCollection.keys():
                self._bCollection[bid] = bobj
    def bExists(self,bid):
        if self._bCollection is not None:
            if bid in self._bCollection.keys():
                return True
        return False
    def removeBook(self,id):
        if self.bExists(id):
            x = self._bCollection[id]
            del self._bCollection[id]
            return x
    def printBBooks(self):
        retMsg = ''+str(self._pid)+','
        for x in self._bCollection.keys():
            retMsg = retMsg + x +': '+self._bCollection[x].get_title()+','
        return retMsg

    def getBook(self,id):
        if self.bExists(id):
            return self._bCollection[id]
    def regIn(self,id):
        if id in self._eventR:
            return False #Register failed
        else:
            self._eventR.append(id)
            return True #Register Successful
    def deReg(self,id):
        if id in self._eventR:
            self._eventR.remove(id)
            return True
        else:
            return False

    def inE(self,id):
        if id in self._eventR:
            return True
        else:
            return False