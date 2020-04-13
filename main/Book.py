import threading

'''
Class: Book
Attributes:
    _id: Book identification
    _title: Book title
    _lock: threading.Lock object used as a semaphore variable
'''
class Book():
    _id = None
    _title = None
    _lock = None

    '''
    Construction of a single book object, including it's own individual thread lock
    '''
    def __init__(self,id,title):
        self._id = id
        self._title = title
        self._lock = threading.Lock()
    def get_id(self):
        return self._id

    def get_title(self):
        return self._title

    '''
    Invokes acquire lock from the object thread.Lock which if the lock is 
    '''
    def acqLock(self):
        return self._lock.acquire()

    '''
    Releases the lock invoking threading.notifyAll() to all threads in waiting state by Book.acqLock() 
    and only a single thread will acquire the lock and all others will be back in waiting state
    '''
    def relLock(self):
        self._lock.release()

    '''
    Boolean function returning true if the Book's lock is acquired by a thread
    '''
    def checkLock(self):
        return self._lock.locked()
