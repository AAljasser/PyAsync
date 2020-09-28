import unittest
import sys
#This to allow the unittest module to include the source code to test
sys.path.append('../')
from main.Library import Library
from main.IndState import IndState as iD
from main.Book import Book
import logging
from datetime import datetime
import time


class TestingLibrarySystem(unittest.TestCase):
    logging.basicConfig(filename='library.log', level=logging.INFO)
    logging.info("\n\n\n\n\n\n\n\n"+str(datetime.now()))
    #Definition of a library
    #Test Complete
    #def test_libDef(self):
    #    x = Library()
    #    self.assertTrue(type(x) is Library)

    #Test Completed and successful 
    def test_singleIns(self):
        x = Library()
        y = Library()
        self.assertTrue(x == y)

    def test_login(self):
        x = Library()
        #Provided the information, we check if this information exists in the library
        #   if it exists then we reroute the state of the client accordingly
        info = ['admin']
        self.assertEqual(x.userLogin(info),iD.A_MENU)

    def test_staffCreation(self):
        x = Library()
        id = 'S1001'
        x.createStaff(id)
        self.assertTrue(x.staffExists(id))

    def test_libraryAddingBook(self):
        id = 'b1008'
        title = 'Hunger Games 8'
        Library().addBook(id,title)
        self.assertTrue(Library().bookExists('b1008'))

    def test_checkOutSystem(self):
        patron = 'p1000'
        id = 'b1006'
        title = 'Hunger Games 6'
        Library().addBook(id,title)
        Library().borrow(patron,id)
        #TODO: must borrow book beforehand
        Library().checkOut(patron)

    def test_uncheckBook(self):
        patron = 'p1000'
        id = 'b1009'
        title = 'Hunger Games 6'
        Library().addBook(id,title)
        Library().borrow(patron,id)
        Library().uncheck(patron,id)

    def test_eventCreation(self):
        eventID = 'e1000'
        Library().createEvent(eventID)
        self.assertTrue(Library().eventExists(eventID))

    def test_eventJoinNoBorrow(self):
        eventId = 'e1001'
        pid = 'p1000'
        Library().regEvent(eventId,pid,bid=None)
        self.assertTrue(Library().getPatron(pid).inE(eventId))

    def test_eventJoin(self):
        eventId = 'e1001'
        pid = 'p1000'
        bid = 'b1000'
        Library().regEvent(eventId,pid,bid=bid)
        self.assertTrue(Library().getPatron(pid).bExists(bid))
        self.assertTrue(Library().getPatron(pid).inE(eventId))

    def test_cartAutoReturn(self):
        patron = 'p1000'
        id = 'b1012'
        title = 'Hunger Games 6'
        Library().addBook(id,title)
        Library().borrow(patron,id)
        time.sleep(31)
        self.assertFalse(Library().checked(id))

    def test_labCreation(self):
        lab = 'l1000'
        openTime = 10 #Seconds
        Library().createLab(lab,openTime)
        self.assertTrue(Library().labExists(lab))

    def test_labJoining(self):
        patron = 'p1000'
        lab = 'l1000'
        Library().createLab(lab,10)
        self.assertTrue(Library().joinLab(patron,lab))
        self.assertTrue(Library().getLab(lab).isIn(patron))

if __name__== '__main__':
    unittest.main()