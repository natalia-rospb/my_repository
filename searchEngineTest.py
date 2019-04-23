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

class ContextWindowTest(unittest.TestCase):

    def setUp(self):
        self.testindexer = indexer.Indexer('database')

    def test_context_window_search_one_token_several_files(self):
        windowslist = []
        testfile = open("text.txt", 'w')
        testfile.write("There are only kittens!")
        testfile.close()
        testfile2 = open("text2.txt", 'w')
        testfile2.write("only...")
        testfile2.close()
        self.testindexer.index_with_lines("text.txt")
        self.testindexer.index_with_lines("text2.txt")
        testsearch = search_engine.SearchEngine('database')
        searchresult = testsearch.search_by_token("only")
        windows = search_engine.ContextWindow.get_context_window_one_position_one_file(indexer.Position_with_lines(10,14,0),"text.txt",2,1)
        windows2 = search_engine.ContextWindow.get_context_window_one_position_one_file(indexer.Position_with_lines(0,4,0),"text2.txt",2,1)
        windowslist = search_engine.ContextWindow.get_context_window(searchresult,2,1)
        expectedwindowresult1 = search_engine.ContextWindow("only",
                        indexer.Position_with_lines(0,4,0),
                        search_engine.WindowPosition(0,4,0,"text2.txt"))
        expectedwindowresult2 = search_engine.ContextWindow("There are only kittens",
                        indexer.Position_with_lines(10,14,0),
                        search_engine.WindowPosition(0,22,0,"text.txt"))
        self.assertEqual(expectedwindowresult1, windows2)
        self.assertEqual(expectedwindowresult2, windows)
        self.assertTrue(expectedwindowresult1 in windowslist)
        self.assertTrue(expectedwindowresult2 in windowslist)
        
    def test_context_window_search_several_tokens_several_files(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only fluffy kittens!")
        testfile.close()
        testfile2 = open("text2.txt", 'w')
        testfile2.write("only kittens and puppies...")
        testfile2.close()
        self.testindexer.index_with_lines("text2.txt")
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        searchresult = testsearch.several_tokens_search("only kittens")

        # context '0,0'
        windowslist = search_engine.ContextWindow.get_context_window(searchresult,0,0)
        print(windowslist)
        expectedwindowresult1 = search_engine.ContextWindow("There are only fluffy kittens",
                        [indexer.Position_with_lines(10,14,0),indexer.Position_with_lines(22,29,0)],
                        search_engine.WindowPosition(6,29,0,"text.txt"))
        expectedwindowresult2 = search_engine.ContextWindow("only kittens and puppies",
                        [indexer.Position_with_lines(0,4,0),indexer.Position_with_lines(5,12,0)],
                        search_engine.WindowPosition(0,12,0,"text2.txt"))
        self.assertTrue(expectedwindowresult1 in windowslist)
        self.assertTrue(expectedwindowresult2 in windowslist)

        # context '1,1'
        windowslist = search_engine.ContextWindow.get_context_window(searchresult,1,1)
        expectedwindowresult1 = search_engine.ContextWindow("There are only fluffy kittens",
                        [indexer.Position_with_lines(10,14,0),indexer.Position_with_lines(22,29,0)],
                        search_engine.WindowPosition(6,29,0,"text.txt"))
        expectedwindowresult2 = search_engine.ContextWindow("only kittens and puppies",
                        [indexer.Position_with_lines(0,4,0),indexer.Position_with_lines(5,12,0)],
                        search_engine.WindowPosition(0,16,0,"text2.txt"))
        self.assertTrue(expectedwindowresult1 in windowslist)
        self.assertTrue(expectedwindowresult2 in windowslist)
        
        # context '2,2'
        windowslist = search_engine.ContextWindow.get_context_window(searchresult,2,2)
        expectedwindowresult1 = search_engine.ContextWindow("There are only fluffy kittens",
                        [indexer.Position_with_lines(10,14,0),indexer.Position_with_lines(22,29,0)],
                        search_engine.WindowPosition(0,29,0,"text.txt"))
        expectedwindowresult2 = search_engine.ContextWindow("only kittens and puppies",
                        [indexer.Position_with_lines(0,4,0),indexer.Position_with_lines(5,12,0)],
                        search_engine.WindowPosition(0,24,0,"text2.txt"))
        self.assertTrue(expectedwindowresult1 in windowslist)
        self.assertTrue(expectedwindowresult2 in windowslist)
        
        # context '3,3'
        windowslist = search_engine.ContextWindow.get_context_window(searchresult,3,3)
        expectedwindowresult1 = search_engine.ContextWindow("There are only fluffy kittens",
                        [indexer.Position_with_lines(10,14,0),indexer.Position_with_lines(22,29,0)],
                        search_engine.WindowPosition(0,29,0,"text.txt"))
        expectedwindowresult2 = search_engine.ContextWindow("only kittens and puppies",
                        [indexer.Position_with_lines(0,4,0),indexer.Position_with_lines(5,12,0)],
                        search_engine.WindowPosition(0,24,0,"text2.txt"))
        self.assertTrue(expectedwindowresult1 in windowslist)
        self.assertTrue(expectedwindowresult2 in windowslist)

    def tearDown(self):
        self.testindexer.closeDatabase()
        for filename in os.listdir(os.getcwd()):
            if (filename == "database" or filename.startswith('database.')):
                os.remove(filename)
            if (filename == "text" or filename.startswith('text')):
                os.remove(filename)

if __name__=='__main__':
    unittest.main() 
