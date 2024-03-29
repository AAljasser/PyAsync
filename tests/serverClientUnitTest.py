import unittest
import sys
#This to allow the unittest module to include the source code to test
sys.path.append('../')
from main.sClient import sClient
from main.Library import Library
from main.runBG import runBG
import logging
from datetime import datetime


class TestingServerClient(unittest.TestCase):
    logging.basicConfig(filename='library.log', level=logging.INFO)
    logging.info("\n\n\n\n\n\n\n\n"+str(datetime.now()))
    # #Testing Client Server connection
    runBG()
    def test_singleConnection(self):
        #runBG()
        msg = "test"
        ##The server is ran before the unittest is ran
        #sSocket = sServer()
        cSocket = sClient()
        self.assertIsNotNone(cSocket.send(msg))
        cSocket.close()

    def test_MultipleConnection(self):
        #runBG()
        msg = "test"
        ##The server is ran before the unittest is ran
        #sSocket = sServer()
        cSocket = sClient()
        cSocket2= sClient()
        self.assertIsNotNone(cSocket.send(msg))
        self.assertIsNotNone(cSocket2.send(msg))
        cSocket.close()
        cSocket2.close()

    def test_clientCommunication(self):
        #runBG()
        msg = "Hi"
        ##Server is supposed to be ran outside
        cSocket = sClient()
        s = cSocket.send(msg)
        self.assertEqual(s[0], str(-1))
        cSocket.close()

    def test_adminCreateStaff(self):
        # runBG()
        admin = sClient()
        admin.send('admin')
        admin.send('crstaff,S1002')
        self.assertTrue(Library().staffExists("S1002"))
        admin.send('exit')

    def test_staffCreatePatron(self):
        # runBG()
        staff = sClient()
        staff.send('staff,s1000')
        staff.send('crpatron,p1001,jack')
        self.assertTrue(Library().patronExists("p1001"))
        staff.send('exit')

    def test_bookInsertion(self):
        # runBG()
        s = sClient()
        s.send('staff,s1000')
        s.send('addbook,b1001,Hunger Games')
        self.assertTrue(Library().bookExists('b1001'))
        s.send('exit')

    def test_bookBorrow(self):
        # runBG()
        s = sClient()
        s.send('patron,p1000')
        s.send("borrow,b1000")
        self.assertTrue(Library().getPatron('p1000').bExists('b1000'))

    def test_bookReturn(self):
        # runBG()
        s = sClient()
        s.send('patron,p1000')
        s.send("borrow,b1000")
        #UPDATE AFTER ADDING CHECKOUT
        s.send("checkout")
        self.assertTrue(Library().getPatron('p1000').bExists('b1000')) #Here we see that patron has the bookk
        self.assertFalse(Library().bookExists('b1000')) #Here we check that the library doesnt have t he book
        s.send("return,b1000")
        self.assertFalse(Library().getPatron('p1000').bExists('b1000')) # here we see that patron doesnt have the book
        self.assertTrue(Library().bookExists('b1000')) # here we see that alibrary has gotten the book

    def test_bookCheckout(self):
        # runBG()
        s = sClient()
        s.send('patron,p1000')
        s.send("borrow,b1000")
        s.send("checkout")
        self.assertTrue(Library().getPatron('p1000').bExists('b1000')) #Here we see that patron has the bookk
        self.assertFalse(Library().bookExists('b1000')) #Here we check that the library doesnt have t he book

    def test_eventWB(self):
        #Event registering (without) borrowing book
        # runBG()
        s = sClient()
        s.send('patron,p1000')
        s.send('event,e1001')
        self.assertTrue(Library().getPatron('p1000').inE('e1001'))

    def test_event(self):
        #Event registering (with) borrowing book
        # runBG()
        s = sClient()
        s.send('patron,p1000')
        s.send('event,e1001,b1000')
        self.assertTrue(Library().getPatron('p1000').bExists('b1000'))
        self.assertTrue(Library().getPatron('p1000').inE('e1001'))

    def test_staffEventCreation(self):
        # runBG()
        staff = sClient()
        staff.send('staff,s1000')
        staff.send('cevent,e1010')
        self.assertTrue(Library().eventExists('e1010'))

    def test_staffCreateLab(self):
        # runBG()
        staff = sClient()
        staff.send('staff,s1000')
        staff.send('clab,l1010')
        self.assertTrue(Library().labExists('l1010'))

    def test_patronJoinLab(self):
        # runBG()
        staff = sClient()
        staff.send('staff,s1000')
        staff.send('clab,l1000')
        patron = sClient()
        patron.send('patron,p1000')
        patron.send('lab,l1000') #This will cause the code to be waiting to get in (30 seconds)
        self.assertTrue(Library().getLab('l1000').isIn('p1000'))


if __name__== '__main__':
    unittest.main()