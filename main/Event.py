import threading

'''
Class: Event
Description: An Event object part of Library system
Attributes:
    _id: Event identification
    _title: Event title
    _elock: threading.Lock object used as a semaphore variable
    _regP: List of registered patrons
'''
class Event():
    _id = None
    _title = None
    _eLock = None
    _regP = []

    def __init__(self,id,title):
        self._id = id
        self._title = title
        self._eLock = threading.Lock()
    '''
    Boolean function returning true if the Book's lock is acquired by a thread
    '''
    def cLock(self):
        return self._eLock.locked()
    '''
    Invokes acquire lock from the object thread.Lock which if the lock is 
    '''
    def acqL(self):
        return self._eLock.acquire()
    '''
    Releases the lock invoking threading.notifyAll() to all threads in waiting state by Book.acqLock() 
    and only a single thread will acquire the lock and all others will be back in waiting state
    '''
    def reL(self):
        self._eLock.release()
    '''
    Registers patron's identification into the _regP (List of registered)
        Return: True if user isn't already registered in the event, False otherwise
    '''
    def register(self,id):
        if id in self._regP:
            return False #Register failed
        else:
            self._regP.append(id)
            return True #Register Successful
    '''
    Deregisters patron's identification from the _regP (List of registered)
        Return: True if user is already registered in the event, False otherwise
    '''
    def deregister(self,id):
        if id in self._regP:
            self._regP.remove(id)
            return True
        else:
            return False