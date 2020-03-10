import unittest
from main.Library import Library
from IndState import IndState as iD
from main.Book import Book
import logging


class TestingLibrarySystem(unittest.TestCase):
    logging.basicConfig(filename='library.log',level=logging.INFO)
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

    def test_eventCreation(self):
        eventID = 'e1000'
        Library().createEvent(eventID)
        self.assertTrue(Library().eventExists(eventID))

    def test_eventJoinNoBorrow(self):
        eventId = 'e1001'
        pid = 'p1000'
        Library().regEvent(id,pid,bid=None)

    def test_eventJoin(self):
        eventId = 'e1001'
        pid = 'p1000'
        bid = 'b1000'
        Library().regEvent(id,pid,bid=bid)
        self.



if __name__== '__main__':
    unittest.main()