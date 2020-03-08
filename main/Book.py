import threading
class Book():
    _id = None
    _title = None
    _lock = None

    def __init__(self,id,title):
        self._id = id
        self._title = title
        self._lock = threading.Lock()
    def get_id(self):
        return self._id
    def get_title(self):
        return self._title
    def acqLock(self):
        return self._lock.acquire()
    def relLock(self):
        self._lock.release()
    def checkLock(self):
        return self._lock.locked()