

class Patreon():
    _pid = None
    _pname = None
    _bCollection = {} # Dic
    def __init__(self,name,id):
        self._pname = name
        self._pid = id
    def get_id(self):
        return self._pid
    def get_name(self):
        return self._pname
    def addBook(self,bid,bobj):
        ##FOR Now only add books that do not exists already, since duplicate key could cause latter issue
        if bid not in self._bCollection.keys():
            self._bCollection[bid] = bobj
    def bExists(self,bid):
        if bid in self._bCollection.keys():
            return True
        else:
            return False