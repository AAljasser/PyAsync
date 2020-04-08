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