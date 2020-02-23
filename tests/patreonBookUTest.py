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
    def test_patreonAddBook(self):
        title = 'Hunger Games'
        id = 'b1001'
        b = Book(title,id)
        namep ='Samuel Jackson'
        idp = 'p1001'
        d = Patreon(namep,idp)
        d.addBook(b.get_id(),b)
        self.assertTrue(d.bExists(b.get_id()))

    def test_returnBook(self):
        title = 'Hunger Games'
        id = 'b1001'
        b = Book(title,id)
        namep ='Samuel Jackson'
        idp = 'p1001'
        d = Patreon(namep,idp)
        d.addBook(b.get_id(),b)
        x = d.removeBook(b.get_id()) #removing book, returns book objectr
        self.assertEqual(x,b)




if __name__== '__main__':
    unittest.main()