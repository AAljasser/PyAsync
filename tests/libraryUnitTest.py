import unittest
from main.Library import Library
from IndState import IndState as iD
from main.Book import Book

class TestingLibrarySystem(unittest.TestCase):

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
        id = 'b1001'
        title = 'Hunger Games'
        Library().addBook(id,title)
        self.assertTrue(Library().bookExists('b1001'))


if __name__== '__main__':
    unittest.main()