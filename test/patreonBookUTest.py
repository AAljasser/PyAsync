import unittest

class TestingPatreonBook(unittest.TestCase):
    def test_patreonCreation(self):
        name ='Samuel Jackson'
        id = 'p1001'
        b = Book(name,id)



if __name__== '__main__':
    unittest.main()