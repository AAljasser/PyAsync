import unittest
from main.Patron import Patron
from main.Book import Book

class TestingPatronBook(unittest.TestCase):
    def test_patronCreation(self):
        name ='Samuel Jackson'
        id = 'p1001'
        b = Patron(name,id)

    def test_bookCreation(self):
        title = 'Hunger Games'
        id = 'b1001'
        b = Book(id,title)
        self.assertEqual(title, b.get_title())
        self.assertEqual(id, b.get_id())
    def test_patronAddBook(self):
        title = 'Hunger Games'
        id = 'b1001'
        b = Book(title,id)
        namep ='Samuel Jackson'
        idp = 'p1001'
        d = Patron(namep,idp)
        d.addBook(b.get_id(),b)
        self.assertTrue(d.bExists(b.get_id()))

    def test_returnBook(self):
        title = 'Hunger Games'
        id = 'b1001'
        b = Book(title,id)
        namep ='Samuel Jackson'
        idp = 'p1001'
        d = Patron(namep,idp)
        d.addBook(b.get_id(),b)
        x = d.removeBook(b.get_id()) #removing book, returns book objectr
        self.assertEqual(x.get_id(),b.get_id())
        self.assertFalse(d.bExists(b.get_id()))





if __name__== '__main__':
    unittest.main()