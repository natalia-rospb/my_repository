import unittest
import indexer
import shelve


class PositionTest(unittest.TestCase):

    def setUp(self):
        self.t = indexer.Position()

    def test_equal(self, obj):
        self.wordbeg = 1
        obj.wordbeg = 1
        self.wordend = 6
        obj.wordend = 6
        self.assertTrue(self.__eq__(obj))

    def test_not_equal(self, obj):
        self.wordbeg = 1
        obj.wordbeg = 2
        self.wordend = 6
        obj.wordend = 6
        self.assertFalse(self.__eq__(obj))

    def test_not_equal_all(self, obj):
        self.wordbeg = 4
        obj.wordbeg = 2
        self.wordend = 5
        obj.wordend = 3
        self.assertFalse(self.__eq__(obj))
        

class IndexerTest(unittest.TestCase):
    
    def setUp(self):
        self.testindexer = indexer.Indexer()
        self.database = shelve.open("Плутон.txt", writeback=True)

    def test_error_input_int(self):
        with self.assertRaises(TypeError)
           self.indexer.index(14198)
           
    def test_error_input_bool(self):
        with self.assertRaises(TypeError)
           self.indexer.index(True)
           
    def test_error_empty_input(self):
        with self.assertRaises(TypeError)
           self.indexer.index()    

    def test_error_wrong_path
        with self.asserRaises(FileNotFoundError)
            self.indexer.index("Текст.txt")
            
    def test_input_empty_text(self):
        testfile = open("text.txt", 'w' )
        testfile.write("")
        self.assertEqual(self.indexer.index("text.txt"),
                         dict(self.database)=={})
        os.remove("text.txt")

    def test_input_one_word(self):
        testfile = open("text.txt", 'w' )
        testfile.write("sun")
        self.assertEqual(self.indexer.index("text.txt"),
                         dict(self.database)=={"sun": {"text.txt": [Position(0,2)]}})
        os.remove("text.txt")
        
    def test_input_two_same_words(self):
        testfile = open("text.txt", 'w' )
        testfile.write("sun sun")
        self.assertEqual(self.indexer.index("text.txt"),
                         dict(self.database)=={"sun": {"text.txt": [Position(0,2); Position(4,6)]}})
        os.remove("text.txt")
        
