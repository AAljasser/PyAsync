import unittest
from main.Library import Library


class TestingLibrarySystem(unittest.TestCase):

    #Definition of a library
    def test_libDef(self):
        x = Library()
        self.assertTrue(type(x) is Library)

if __name__== '__main__':
    unittest.main()