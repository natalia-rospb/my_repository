import indexer
import unittest
import os
import shelve
import search_engine


class SearchEngineSimpleTest(unittest.TestCase):

    def setUp(self):
        self.testindexer = indexer.Indexer('database')
        
    def test_query_int(self):
        testsearch = search_engine.SearchEngine('database')
        with self.assertRaises(TypeError):
            resulteddictionary = dict(testsearch.search_by_token(126))

    def test_several_tokens(self):
        testsearch = search_engine.SearchEngine('database')
        with self.assertRaises(TypeError):
            resulteddictionary = dict(testsearch.search_by_token('mom', 'dad'))

    def test_search_in_empty_database(self):
        testfile = open("text.txt", 'w')
        testfile.write("")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        expectedresult = {}
        resulteddictionary = testsearch.search_by_token("puppy")
        self.assertEqual(resulteddictionary, expectedresult)

    def test_search_with_empty_query(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only kittens!")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        expectedresult = {}
        resulteddictionary = testsearch.search_by_token("")
        self.assertIsInstance(resulteddictionary, dict)
        self.assertEqual(resulteddictionary, expectedresult)

    def test_search_inexistent_token(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only kittens!")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        expectedresult = {}
        resulteddictionary = testsearch.search_by_token("puppy")
        self.assertIsInstance(resulteddictionary, dict)
        self.assertEqual(resulteddictionary, expectedresult)

    def test_search_one_token_one_file(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only kittens!")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        expectedresult = dict({"There": {"text.txt":[indexer.Position_with_lines(0,5,0)]},
            "are": {"text.txt":[indexer.Position_with_lines(6,9,0)]},
            "only": {"text.txt":[indexer.Position_with_lines(10,14,0)]},
            "kittens": {"text.txt":[indexer.Position_with_lines(15,22,0)]}})
        resulteddictionary = dict(shelve.open('database'))
        self.assertEqual(resulteddictionary, expectedresult)
        searchresulteddictionary = testsearch.search_by_token("only")
        expectedsearchresult = {"text.txt": [indexer.Position_with_lines(10,14,0)]}
        self.assertIsInstance(searchresulteddictionary, dict)
        self.assertEqual(searchresulteddictionary, expectedsearchresult)

    def test_search_one_token_several_files(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only kittens!")
        testfile.close()
        testfile2 = open("text2.txt", 'w')
        testfile2.write("only...")
        testfile2.close()
        self.testindexer.index_with_lines("text.txt")
        self.testindexer.index_with_lines("text2.txt")
        testsearch = search_engine.SearchEngine('database')
        searchresulteddictionary = testsearch.search_by_token("only")
        expectedsearchresult = {"text.txt": [indexer.Position_with_lines(10,14,0)],
                                "text2.txt": [indexer.Position_with_lines(0,4,0)]}
        self.assertIsInstance(searchresulteddictionary, dict)
        self.assertEqual(searchresulteddictionary, expectedsearchresult)

    def tearDown(self):
        self.testindexer.closeDatabase()
        for filename in os.listdir(os.getcwd()):
            if (filename == "database" or filename.startswith('database.')):
                os.remove(filename)
            if (filename == "text" or filename.startswith('text')):
                os.remove(filename)


class SearchEngineComplexTest(unittest.TestCase):

    def setUp(self):
        self.testindexer = indexer.Indexer('database')
        
    def test_query_int(self):
        testsearch = search_engine.SearchEngine('database')
        with self.assertRaises(TypeError):
            resulteddictionary = dict(testsearch.several_tokens_search(126))

    def test_search_in_empty_database(self):
        testfile = open("text.txt", 'w')
        testfile.write("")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        expectedresult = {}
        resulteddictionary = testsearch.several_tokens_search("puppy kitty")
        self.assertEqual(resulteddictionary, expectedresult)

    def test_search_with_empty_query(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only kittens!")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        expectedresult = {}
        resulteddictionary = testsearch.several_tokens_search("")
        self.assertIsInstance(resulteddictionary, dict)
        self.assertEqual(resulteddictionary, expectedresult)

    def test_search_inexistent_token(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only kittens!")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        expectedresult = {}
        resulteddictionary = testsearch.several_tokens_search("puppy")
        self.assertIsInstance(resulteddictionary, dict)
        self.assertEqual(resulteddictionary, expectedresult)

    def test_search_one_token_one_file(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only kittens!")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        searchresulteddictionary = testsearch.several_tokens_search("only")
        expectedsearchresult = {"text.txt": [indexer.Position_with_lines(10,14,0)]}
        self.assertIsInstance(searchresulteddictionary, dict)
        self.assertEqual(searchresulteddictionary, expectedsearchresult)

    def test_search_one_token_several_files(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only kittens!")
        testfile.close()
        testfile2 = open("text2.txt", 'w')
        testfile2.write("only...")
        testfile2.close()
        self.testindexer.index_with_lines("text.txt")
        self.testindexer.index_with_lines("text2.txt")
        testsearch = search_engine.SearchEngine('database')
        searchresulteddictionary = testsearch.several_tokens_search("only")
        expectedsearchresult = {"text.txt": [indexer.Position_with_lines(10,14,0)],
                                "text2.txt": [indexer.Position_with_lines(0,4,0)]}
        self.assertIsInstance(searchresulteddictionary, dict)
        self.assertEqual(searchresulteddictionary, expectedsearchresult)

    def test_several_tokens_one_file(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only kittens!")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        searchresulteddictionary = testsearch.several_tokens_search("only kittens")
        expectedsearchresult = {"text.txt": [indexer.Position_with_lines(10,14,0),
                                             indexer.Position_with_lines(15,22,0)]}
        self.assertEqual(searchresulteddictionary, expectedsearchresult)
        searchresulteddictionary = testsearch.several_tokens_search("only kittens and")
        expectedsearchresult = {}
        self.assertEqual(searchresulteddictionary, expectedsearchresult)
        
    def test_several_tokens_several_files(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only kittens!")
        testfile.close()
        testfile2 = open("text2.txt", 'w')
        testfile2.write("only kittens and puppies...")
        testfile2.close()
        self.testindexer.index_with_lines("text2.txt")
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        searchresulteddictionary = testsearch.several_tokens_search("only kittens")
        expectedsearchresult = {"text.txt": [indexer.Position_with_lines(10,14,0),
                                             indexer.Position_with_lines(15,22,0)],
                                "text2.txt": [indexer.Position_with_lines(0,4,0),
                                              indexer.Position_with_lines(5,12,0)]}
        self.assertEqual(searchresulteddictionary, expectedsearchresult)
        searchresulteddictionary = testsearch.several_tokens_search("only kittens and")
        expectedsearchresult = {"text2.txt": [indexer.Position_with_lines(0,4,0),
                                              indexer.Position_with_lines(5,12,0),
                                              indexer.Position_with_lines(13,16,0)]}
        self.assertEqual(searchresulteddictionary, expectedsearchresult)
                    
    def tearDown(self):
        self.testindexer.closeDatabase()
        for filename in os.listdir(os.getcwd()):
            if (filename == "database" or filename.startswith('database.')):
                os.remove(filename)
            if (filename == "text" or filename.startswith('text')):
                os.remove(filename)

if __name__=='__main__':
    unittest.main() 
