import unittest
import indexer
import shelve
import os


class PositionTest(unittest.TestCase):

    def test_equal(self):
        a = indexer.Position(1, 6)
        b = indexer.Position(1, 6)
        self.assertEqual(a, b)

    def test_not_equal(self):
        a = indexer.Position(2, 5)
        b = indexer.Position(4, 6)
        self.assertNotEqual(a, b)


class PositionWithLinesTest(unittest.TestCase):

    def test_equal(self):
        a = indexer.Position_with_lines(1, 6, 3)
        b = indexer.Position_with_lines(1, 6, 3)
        self.assertEqual(a, b)

    def test_not_equal(self):
        a = indexer.Position_with_lines(2, 5, 1)
        b = indexer.Position_with_lines(4, 6, 1)
        self.assertNotEqual(a, b)
        

class IndexerTest(unittest.TestCase):
    
    def setUp(self):
        self.testindexer = indexer.Indexer('database')

    def test_error_wrong_path(self):
        with self.assertRaises(FileNotFoundError):
            self.testindexer.index("test.txt")
            self.testindexer.closeDatabase()

    def test_empty_input(self):
        testfile = open("text.txt", 'w' )
        testfile.write("")
        testfile.close()
        expectedresult = dict({})
        self.testindexer.index("text.txt")
        resulteddictionary = dict(shelve.open('database'))
        self.assertEqual(resulteddictionary, expectedresult)        

    def test_input_one_word(self):
        testfile = open("text.txt", 'w' )
        testfile.write("sun")
        testfile.close()
        expectedresult = dict({"sun": {"text.txt": [indexer.Position(0,3)]}})
        self.testindexer.index("text.txt")
        resulteddictionary = dict(shelve.open('database'))
        self.assertEqual(resulteddictionary, expectedresult)
        
    def test_input_two_same_words(self):
        testfile = open("text.txt", 'w' )
        testfile.write("sun sun")
        testfile.close()
        expectedresult = dict({"sun": {"text.txt": [indexer.Position(0,3),
                                                    indexer.Position(4,7)]}})
        self.testindexer.index("text.txt")
        resulteddictionary = dict(shelve.open('database'))
        self.assertEqual(resulteddictionary, expectedresult)

    def test_input_two_files(self):
        testfile = open("text.txt", 'w' )
        testfile.write("sun")
        testfile.close()
        testfile2 = open("text2.txt", 'w' )
        testfile2.write("sun")
        testfile2.close()
        expectedresult = dict({"sun": {"text.txt": [indexer.Position(0,3)],
                               "text2.txt": [indexer.Position(0,3)]}})
        self.testindexer.index("text.txt")
        self.testindexer.index("text2.txt")
        resulteddictionary = dict(shelve.open('database'))
        self.assertEqual(resulteddictionary, expectedresult)

    def test_input_sentence(self):
        testfile = open("text.txt", 'w' )
        testfile.write("This is a sentence sentence.")
        testfile.close()
        expectedresult = dict({"This": {"text.txt": [indexer.Position(0,4)]},
                            "is": {"text.txt": [indexer.Position(5,7)]},
                            "a": {"text.txt": [indexer.Position(8,9)]},
                            "sentence": {"text.txt": [indexer.Position(10,18),
                                                    indexer.Position(19,27)]}})
        self.testindexer.index("text.txt")
        resulteddictionary = dict(shelve.open('database'))
        self.assertEqual(resulteddictionary, expectedresult)

    def tearDown(self):
        self.testindexer.closeDatabase()
        for filename in os.listdir(os.getcwd()):
            if (filename == "database" or filename.startswith('database.')):
                os.remove(filename)
            if "text.txt" in os.listdir(os.getcwd()):
                os.remove("text.txt")


class IndexerWithLinesTest(unittest.TestCase):
    
    def setUp(self):
        self.testindexer = indexer.Indexer('database')

    def test_error_wrong_path(self):
        with self.assertRaises(FileNotFoundError):
            self.testindexer.index_with_lines("test.txt")
            self.testindexer.closeDatabase()

    def test_empty_input(self):
        testfile = open("text.txt", 'w' )
        testfile.write("")
        testfile.close()
        expectedresult = dict({})
        self.testindexer.index_with_lines("text.txt")
        resulteddictionary = dict(shelve.open('database'))
        self.assertEqual(resulteddictionary, expectedresult)        

    def test_input_one_word(self):
        testfile = open("text.txt", 'w' )
        testfile.write("sun")
        testfile.close()
        expectedresult = dict({"sun": {"text.txt":[indexer.Position_with_lines(0,3,0)]}})
        self.testindexer.index_with_lines("text.txt")
        resulteddictionary = dict(shelve.open('database'))
        self.assertEqual(resulteddictionary, expectedresult)
        
    def test_input_two_same_words(self):
        testfile = open("text.txt", 'w' )
        testfile.write("sun sun")
        testfile.close()
        expectedresult = dict({"sun": {"text.txt": [indexer.Position_with_lines(0,3,0),
                                                    indexer.Position_with_lines(4,7,0)]}})
        self.testindexer.index_with_lines("text.txt")
        resulteddictionary = dict(shelve.open('database'))
        self.assertEqual(resulteddictionary, expectedresult)

    def test_input_two_files(self):
        testfile = open("text.txt", 'w' )
        testfile.write("sun")
        testfile.close()
        testfile2 = open("text2.txt", 'w' )
        testfile2.write("sun")
        testfile2.close()
        expectedresult = dict({"sun": {"text.txt": [indexer.Position_with_lines(0,3,0)],
                               "text2.txt": [indexer.Position_with_lines(0,3,0)]}})
        self.testindexer.index_with_lines("text.txt")
        self.testindexer.index_with_lines("text2.txt")
        resulteddictionary = dict(shelve.open('database'))
        self.assertEqual(resulteddictionary, expectedresult)

    def test_input_sentence(self):
        testfile = open("text.txt", 'w' )
        testfile.write("This is a sentence \nsentence.")
        testfile.close()
        expectedresult = dict({"This": {"text.txt": [indexer.Position_with_lines(0,4,0)]},
                            "is": {"text.txt": [indexer.Position_with_lines(5,7,0)]},
                            "a": {"text.txt": [indexer.Position_with_lines(8,9,0)]},
                            "sentence": {"text.txt": [indexer.Position_with_lines(10,18,0),
                                                    indexer.Position_with_lines(0,8,1)]}})
        self.testindexer.index_with_lines("text.txt")
        resulteddictionary = dict(shelve.open('database'))
        self.assertEqual(resulteddictionary, expectedresult)

    def tearDown(self):
        self.testindexer.closeDatabase()
        for filename in os.listdir(os.getcwd()):
            if (filename == "database" or filename.startswith('database.')):
                os.remove(filename)
            if "text.txt" in os.listdir(os.getcwd()):
                os.remove("text.txt")

if __name__ == '__main__':
    unittest.main()        
