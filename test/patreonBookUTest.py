import unittest
from main.Patreon import Patreon

class TestingPatreonBook(unittest.TestCase):
    def test_patreonCreation(self):
        name ='Samuel Jackson'
        id = 'p1001'
        b = Patreon(name,id)
        



if __name__== '__main__':
    unittest.main()