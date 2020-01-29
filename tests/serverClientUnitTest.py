import unittest
from main.sServer import sServer
from main.sClient import sClient
from main.Library import Library
from tests.runBG import runBG


class TestingServerClient(unittest.TestCase):

    # #Testing Client Server connection
    # def test_singleConnection(self):
    #     #runBG()
    #     msg = "test"
    #     ##The server is ran before the unittest is ran
    #     #sSocket = sServer()
    #     cSocket = sClient()
    #     self.assertIsNotNone(cSocket.send(msg))
    #     cSocket.close()

    # def test_MultipleConnection(self):
    #     #runBG()
    #     msg = "test"
    #     ##The server is ran before the unittest is ran
    #     #sSocket = sServer()
    #     cSocket = sClient()
    #     cSocket2= sClient()
    #     self.assertIsNotNone(cSocket.send(msg))
    #     self.assertIsNotNone(cSocket2.send(msg))
    #     cSocket.close()
    #     cSocket2.close()

    # def test_clientCommunication(self):
    #     #runBG()
    #     msg = "Hi"
    #     ##Server is supposed to be ran outside
    #     cSocket = sClient()
    #     s = cSocket.send(msg)
    #     self.assertEqual(s[0], str(-1))
    #     cSocket.close()

    def test_adminCreateStaff(self):
        runBG()
        admin = sClient()
        admin.send('admin')
        admin.send('crstaff,S1002')
        self.assertTrue(Library().staffExists("S1002"))
        admin.send('exit')



if __name__== '__main__':
    unittest.main()