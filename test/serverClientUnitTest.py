import unittest
from main.Library import Library


class TestingServerClient(unittest.TestCase):

    #Testing Client Server connection
    def test_singleConnection(self):
        msg = "test"
        sSocket = sSocket();
        cSocket = cSocket();
        assertEquals(cSocket.send(msg),sSocket.lastRecieved)


if __name__== '__main__':
    unittest.main()