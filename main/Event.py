import threading

class Event():
    _id = None
    _title = None
    _eLock = None
    _regP = []

    def __init__(self,id,title):
        self._id = id
        self._title = title
        self._eLock = threading.Lock()

    def acqL(self):
        return self._eLock.acquire()
    def reL(self):
        self._eLock.release()
    def register(self,id):
        if id in self._regP:
            return False #Register failed
        else:
            self._regP.append(id)
            return True #Register Successful
    def deregister(self,id):
        if id in self._regP:
            self._regP.remove(id)
            return True
        else:
            return False