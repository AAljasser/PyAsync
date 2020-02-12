

class Patreon():
    _pid = None
    _pname = None
    _bCollection = [] # List of books
    def __init__(self,name,id):
        self._pname = name
        self._pid = id
    def get_id(self):
        return self._pid
    def get_name(self):
        return self._pname

