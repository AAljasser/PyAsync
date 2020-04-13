import threading
import logging
import threading


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
        # self._Lock.acquire() ## COMMENT THIS LINE to remove solution
        self._id = lid
        self._timerToOpen = threading.Timer(timer,self.openLab).start()

    def openLab(self):
        logging.info("Lab #"+str(self._id)+" Has been opened")
        self._open = True
        # self._Lock.release() ## COMMENT THIS LINE to remove solution

    def checkLab(self):
        return self._open

    def canGetIn(self):
        if len(self._pGotIn)<self._maxUsers:
            return True
        else:
            return False

    def join(self,pid):
        self._queue.append(pid)

        ## If solution is removed the bottom while loop must be uncommented
        while not self.checkLab():
            None

        ##  SOLUTION TO QueueRACE BEGINS (Comment/Uncomment) to induce/resolve
        # self._Lock.acquire()
        # logging.info("Patron #:"+str(pid)+" checked if infront of queue")
        # while pid not in self._queue[0]: ##Meaning infront of line
        #     logging.info("Patron #:"+str(pid)+" NOT infront of queue")
        #     self._Lock.release()
        #     self._Lock.acquire()
        #     logging.info("Patron #:"+str(pid)+" checked if infront of queue")
        # logging.info("Patron #:"+str(pid)+" Front of queue got in")
        ##SOLUTION BLOCK END

        self._queue.remove(pid)
        if self.canGetIn():
            if pid not in self._pGotIn:
                self._pGotIn.append(pid)
                # self._Lock.release() ## COMMENT THIS LINE to remove solution
                return True
            else:
                # self._Lock.release() ## COMMENT THIS LINE to remove solution
                return False
        else:
            # self._Lock.release() ## COMMENT THIS LINE to remove solution
            return False

    def isIn(self,pid):
        if pid in self._pGotIn:
            return True
        else:
            return False

    def leave(self,pid):
        if pid in self._pGotIn:
            self._pGotIn.remove(pid)
            return True
        else:
            return False