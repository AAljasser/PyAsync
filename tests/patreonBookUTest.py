import unittest
from main.Patreon import Patreon
from main.Book import Book

class TestingPatreonBook(unittest.TestCase):
    def test_patreonCreation(self):
        name ='Samuel Jackson'
        id = 'p1001'
        b = Patreon(name,id)

    def test_bookCreation(self):
        title = 'Hunger Games'
        id = 'b1001'
        b = Book(title,id)
        self.assertEqual(title, b.get_title())
        self.assertEqual(id, b.get_id())



if __name__== '__main__':
    unittest.main()