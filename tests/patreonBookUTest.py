import unittest
from main.Patreon import Patreon

class TestingPatreonBook(unittest.TestCase):
    def test_patreonCreation(self):
        name ='Samuel Jackson'
        id = 'p1001'
        b = Patreon(name,id)

    def test_bookCreation(self):
        title = 'Hunger Games'
        id = 'b1001'
        b = Book(name,id)
        self.assertIsInstance(b, Book)



if __name__== '__main__':
    unittest.main()