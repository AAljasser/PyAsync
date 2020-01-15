import unittest
from main import library


class TestingLibrarySystem(unittest.TestCase):

    #Definition of a library
    def test_libDef(self):
        self.assertIsInstance(library(),type(library()))

if __name__== '__main__':
    unittest.main()