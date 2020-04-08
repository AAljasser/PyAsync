import threading
import logging

class Lab():
    _id = None
    _timerToOpen = None
    _open = False # All these are set to False and timer to open will
    _maxUsers = 2 # This is set defaulted to 2 users due to the fact we are focusing on testing the behavior of a queue
    _pGotIn = [] #List of users that were able to get in

    def __init__(self,lid,timer):
        self._id = lid
        self._timerToOpen = threading.Timer(timer,self.openLab).start()

    def openLab(self):
        logging.info("Lab #"+str(self._id)+" Has been opened")
        self._open = True

    def checkLab(self):
        return self._open

    def canGetIn(self):
        if len(self._pGotIn)<self._maxUsers:
            return True
        else:
            return False

    def join(self,pid):
        if self.canGetIn():
            if pid not in self._pGotIn:
                self._pGotIn.append(pid)
                return True
            else:
                return False
        else:
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