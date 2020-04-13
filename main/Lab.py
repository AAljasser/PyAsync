import threading
import logging
import threading

'''
Class: Lab
Description: Computer Lab object part of Library system
Attributes:
    _id: Lab identification
    _timerToOpen: Timer executed after a creation of an Lab event (Time determined by the constructor timer variable)
    _open: A boolean flag used to identify if the lab is open or not (Will be automatically changed by _timerToOpen background object)
    _maxUsers: Maximum number of allowed users into a single Lab (Globally set to max 2)
    _pGotIn: List of patron's inside lab
    _queue: Thread-safe queue for users trying to join lab before _open flag turns to True
    _Lock: thread.Lock object to allow Lab class to be thread safe
'''
class Lab():
    _id = None
    _timerToOpen = None
    _open = False # All these are set to False and timer to open will
    _maxUsers = 2 # This is set defaulted to 2 users due to the fact we are focusing on testing the behavior of a queue
    _pGotIn = None #List of users that were able to get in
    _queue = None
    _Lock = None

    def __init__(self,lid,timer):
        self._pGotIn = []
        self._queue = []
        self._Lock = threading.Lock()
        self._Lock.acquire()
        self._id = lid
        self._timerToOpen = threading.Timer(timer,self.openLab).start()

    '''
    Function that will executed after the set time, the function changes the lab's flag _open to True 
    and releases the lock that is created and acquired in the constructor   
    '''
    def openLab(self):
        logging.info("Lab #"+str(self._id)+" Has been opened")
        self._open = True
        self._Lock.release()

    '''
    Returns the _open flag
    '''
    def checkLab(self):
        return self._open

    '''
    Checks if the maximum users inside the lab is less than the maximum allowed,
     and if space is available return True, otherwise False
    '''
    def canGetIn(self):
        if len(self._pGotIn)<self._maxUsers:
            return True
        else:
            return False

    '''
    Thread-safe implementation of lab join
    '''
    def join(self,pid):
        '''
        The function begins with appending the patron "trying" to joing the lab
        into a list (Python list are thread-safe, therefore we should not face a race condition
        '''
        self._queue.append(pid)
        '''
        Afterward invoking Lab's lock acquire a thread either:
            1. No other thread holds Lab's lock, then code continues
            2. Another thread holds Lab's lock, then current thread invokes wait
        '''
        self._Lock.acquire()
        logging.info("Patron #:"+str(pid)+" checked if infront of queue")
        '''
        After successful lock acquire, the current thread checks if it is the rightful person to join
        this is following the principle of Queue, the check occurs by checking if position 0 in _queue list
        is the thread's patron being processed (Line 80)
        '''
        while pid not in self._queue[0]: ##Meaning infront of line
            logging.info("Patron #:"+str(pid)+" NOT infront of queue")
            '''
            Given the the thread that acquired the lock and it isn't in the front of the queue then
            the thread must release the lock and try to acquire it again (Giving other threads ability to 
            acquire the lock, given one of them is the rightful thread in the queue)
            '''
            self._Lock.release()
            self._Lock.acquire()
            logging.info("Patron #:"+str(pid)+" checked if infront of queue")
        logging.info("Patron #:"+str(pid)+" Front of queue got in")
        '''
        Given rightful thread acquiring Lab's lock, it removes it self from the queue (Python List)
        Continuing processing Patrons registration in lab and before returning out releasing of Lock
        '''
        self._queue.remove(pid)

        if self.canGetIn():
            if pid not in self._pGotIn:
                self._pGotIn.append(pid)
                self._Lock.release()
                return True
            else:
                self._Lock.release()
                return False
        else:
            self._Lock.release()
            return False

    '''
    Boolean function that checks if a certain patron is inside the Lab
    '''
    def isIn(self,pid):
        if pid in self._pGotIn:
            return True
        else:
            return False

    '''
    Returns True if a patron is inside the lab and successfully has be removed outside of the lab, False if the patron isn't inside the Lab
    '''
    def leave(self,pid):
        if pid in self._pGotIn:
            self._pGotIn.remove(pid)
            return True
        else:
            return False