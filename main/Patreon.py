

class Patreon():
    _pid = None
    _pname = None
    _bCollection = None # Dic
    def __init__(self,name,id):
        self._pname = name
        self._pid = id
        self._bCollection = {}
    def get_id(self):
        return self._pid
    def get_name(self):
        return self._pname
    def addBook(self,bid,bobj):
        ##FOR Now only add books that do not exists already, since duplicate key could cause latter issue
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