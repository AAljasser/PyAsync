import unittest
from main.Library import Library


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
        self.assertTrue(x is y)

if __name__== '__main__':
    unittest.main()