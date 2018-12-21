import indexer
import unittest
import os
import shelve
import search_engine


class SearchEngineTest(unittest.TestCase):

    def setUp(self):
        self.testindexer = indexer.Indexer('database')
        self.testsearch = search_engine.SearchEngine('database')

    def test_query_int(self):
        with self.assertRaises(TypeError):
            resulteddictionary = dict(self.testsearch.search_by_token(126))

    def test_several_tokens(self):
        with self.assertRaises(TypeError):
            resulteddictionary = dict(self.testsearch.search_by_token('mom', 'dad'))

    def test_search_in_empty_database(self):
        testfile = open("text.txt", 'w' )
        testfile.write("")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        expectedresult = {}
        resulteddictionary = dict(self.testsearch.search_by_token("puppy"))
        self.assertEqual(resulteddictionary, expectedresult)

    def test_search_with_empty_query(self):
        testfile = open("text.txt", 'w' )
        testfile.write("There are only kittens!")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        expectedresult = {}
        resulteddictionary = self.testsearch.search_by_token("")
        self.assertIsInstance(resulteddictionary, dict)
        self.assertEqual(resulteddictionary, expectedresult)

    def test_search_inexistent_token(self):
        testfile = open("text.txt", 'w' )
        testfile.write("There are only kittens!")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        expectedresult = {}
        resulteddictionary = self.testsearch.search_by_token("puppy")
        self.assertIsInstance(resulteddictionary, dict)
        self.assertEqual(resulteddictionary, expectedresult)

    def test_search_one_token(self):
        testfile = open("text.txt", 'w' )
        testfile.write("There are only kittens!")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        expectedresult = dict({"There": {"text.txt":[indexer.Position_with_lines(0,4,1)]},
            "are": {"text.txt":[indexer.Position_with_lines(6,8,1)]},
            "only": {"text.txt":[indexer.Position_with_lines(10,13,1)]},
            "kittens": {"text.txt":[indexer.Position_with_lines(15,21,1)]}})
        resulteddictionary = dict(shelve.open('database'))
        self.assertEqual(resulteddictionary, expectedresult)
        self.testindexer.closeDatabase()
        searchresulteddictionary = self.testsearch.search_by_token("only")
        expectedsearchresult = {"text.txt": [indexer.Position_with_lines(10,13,1)]}
        self.assertIsInstance(searchresulteddictionary, dict)
        self.assertEqual(searchresulteddictionary, expectedsearchresult)

    def tearDown(self):
        self.testindexer.closeDatabase()
        for filename in os.listdir(os.getcwd()):
            if (filename == "database" or filename.startswith('database.')):
                os.remove(filename)
            if "text.txt" in os.listdir(os.getcwd()):
                os.remove("text.txt")


if __name__=='__main__':
    unittest.main() 
