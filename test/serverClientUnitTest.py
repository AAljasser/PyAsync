import unittest
from main.sServer import sServer
from main.sClient import sClient


class TestingServerClient(unittest.TestCase):

    #Testing Client Server connection
    def test_singleConnection(self):
        msg = "test"
        ##The server is ran before the unittest is ran
        #sSocket = sServer()
        cSocket = sClient()
        self.assertEqual(cSocket.send(msg), None)
        cSocket.close()

    def test_MultipleConnection(self):
        msg = "test"
        ##The server is ran before the unittest is ran
        #sSocket = sServer()
        cSocket = sClient()
        cSocket2= sClient()
        self.assertEqual(cSocket.send(msg), None)
        self.assertEqual(cSocket2.send(msg), None)
        cSocket.close()
        cSocket2.close()

    def test_clientCommunication(self):
        msg = "Hi"
        ##Server is supposed to be ran outside 
        cSocket = sClient()
        cSocket.send(msg)
        self.assertEqual(cSocket.lastRes(), "hi received")
        cSocket.close()



if __name__== '__main__':
    unittest.main()