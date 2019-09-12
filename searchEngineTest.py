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
        expectedresult = dict({"There": {"text.txt":[indexer.Position_with_lines(0, 5, 0)]},
            "are": {"text.txt":[indexer.Position_with_lines(6, 9, 0)]},
            "only": {"text.txt":[indexer.Position_with_lines(10, 14, 0)]},
            "kittens": {"text.txt":[indexer.Position_with_lines(15, 22, 0)]}})
        resulteddictionary = dict(shelve.open('database'))
        self.assertEqual(resulteddictionary, expectedresult)
        searchresulteddictionary = testsearch.search_by_token("only")
        expectedsearchresult = {"text.txt": [indexer.Position_with_lines(10, 14, 0)]}
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
        expectedsearchresult = {"text.txt": [indexer.Position_with_lines(10, 14, 0)],
                                "text2.txt": [indexer.Position_with_lines(0, 4, 0)]}
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
        expectedsearchresult = {"text.txt": [indexer.Position_with_lines(10, 14, 0)]}
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
        expectedsearchresult = {"text.txt": [indexer.Position_with_lines(10, 14, 0)],
                                "text2.txt": [indexer.Position_with_lines(0, 4, 0)]}
        self.assertIsInstance(searchresulteddictionary, dict)
        self.assertEqual(searchresulteddictionary, expectedsearchresult)

    def test_several_tokens_one_file(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only kittens!")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        searchresulteddictionary = testsearch.several_tokens_search("only kittens")
        expectedsearchresult = {"text.txt": [indexer.Position_with_lines(10, 14, 0),
                                             indexer.Position_with_lines(15, 22, 0)]}
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
        expectedsearchresult = {"text.txt": [indexer.Position_with_lines(10, 14, 0),
                                             indexer.Position_with_lines(15, 22, 0)],
                                "text2.txt": [indexer.Position_with_lines(0, 4, 0),
                                              indexer.Position_with_lines(5, 12, 0)]}
        self.assertEqual(searchresulteddictionary, expectedsearchresult)
        searchresulteddictionary = testsearch.several_tokens_search("only kittens and")
        expectedsearchresult = {"text2.txt": [indexer.Position_with_lines(0, 4, 0),
                                              indexer.Position_with_lines(5, 12, 0),
                                              indexer.Position_with_lines(13, 16, 0)]}
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

    def test_context_window_context_window_one_position_one_file(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only kittens!")
        testfile.close()
        testfile2 = open("text2.txt", 'w')
        testfile2.write("only...")
        testfile2.close()
        self.testindexer.index_with_lines("text.txt")
        self.testindexer.index_with_lines("text2.txt")
        testsearch = search_engine.SearchEngine('database')
        window1 = search_engine.ContextWindow.get_context_window_one_position_one_file(indexer.Position_with_lines(0, 4, 0),
                                                                                        "text2.txt", 2, 1)
        window2 = search_engine.ContextWindow.get_context_window_one_position_one_file(indexer.Position_with_lines(10, 14, 0),
                                                                                       "text.txt", 2, 1)
        expectedwindow1 = search_engine.ContextWindow("only",
                        [indexer.Position_with_lines(0, 4, 0)],
                        search_engine.WindowPosition(0, 4, 0, "text2.txt"))
        expectedwindow2 = search_engine.ContextWindow("There are only kittens",
                        [indexer.Position_with_lines(10, 14, 0)],
                        search_engine.WindowPosition(0, 22, 0, "text.txt"))
        self.assertEqual(expectedwindow1, window1)
        self.assertEqual(expectedwindow2, window2)
        windowsdict = testsearch.several_tokens_search_with_customizable_context("only", 2, 1)
        expectedwindowresult = {"text.txt": [search_engine.ContextWindow("There are only kittens",
                                        [indexer.Position_with_lines(10, 14, 0)],
                                        search_engine.WindowPosition(0, 22, 0, "text.txt"))],
                                "text2.txt":[search_engine.ContextWindow("only",
                                        [indexer.Position_with_lines(0, 4, 0)],
                                        search_engine.WindowPosition(0, 4, 0, "text2.txt"))]}
        self.assertEqual(expectedwindowresult, windowsdict)
        
    def test_context_window_search_several_tokens_several_files_0_0(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only fluffy kittens!")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        # context '0,0'
        windowsdict = testsearch.several_tokens_search_with_customizable_context("only kittens", 0, 0)
        expectedwindowresult = {}
        self.assertEqual(expectedwindowresult, windowsdict)

    def test_context_window_search_several_tokens_several_files_1_1(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only fluffy kittens!")
        testfile.close()
        testfile2 = open("text2.txt", 'w')
        testfile2.write("only kittens and puppies...")
        testfile2.close()
        self.testindexer.index_with_lines("text2.txt")
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        # context '1,1'
        windowsdict = testsearch.several_tokens_search_with_customizable_context("only kittens", 1, 1)
        expectedwindowresult = {"text.txt": [search_engine.ContextWindow("There are only fluffy kittens",
                                    [indexer.Position_with_lines(10, 14, 0), indexer.Position_with_lines(22, 29, 0)],
                                     search_engine.WindowPosition(6, 29, 0,"text.txt"))],
                                "text2.txt": [search_engine.ContextWindow("only kittens and puppies",
                                    [indexer.Position_with_lines(0, 4, 0), indexer.Position_with_lines(5, 12, 0)],
                                     search_engine.WindowPosition(0, 16, 0, "text2.txt"))]}
        self.assertEqual(expectedwindowresult, windowsdict)

    def test_context_window_search_several_tokens_several_files_2_2(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only fluffy kittens!")
        testfile.close()
        testfile2 = open("text2.txt", 'w')
        testfile2.write("only kittens and puppies...")
        testfile2.close()
        self.testindexer.index_with_lines("text2.txt")
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        # context '2,2'
        windowsdict = testsearch.several_tokens_search_with_customizable_context("only kittens", 2, 2)
        expectedwindowresult = {"text.txt": [search_engine.ContextWindow("There are only fluffy kittens",
                                    [indexer.Position_with_lines(10, 14, 0), indexer.Position_with_lines(22, 29, 0)],
                                     search_engine.WindowPosition(0, 29, 0, "text.txt"))],
                                "text2.txt": [search_engine.ContextWindow("only kittens and puppies",
                                    [indexer.Position_with_lines(0, 4, 0), indexer.Position_with_lines(5, 12, 0)],
                                     search_engine.WindowPosition(0, 24, 0, "text2.txt"))]}
        self.assertEqual(expectedwindowresult, windowsdict)

    def test_context_window_search_several_tokens_several_files_3_3(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only fluffy kittens!")
        testfile.close()
        testfile2 = open("text2.txt", 'w')
        testfile2.write("only kittens and puppies...")
        testfile2.close()
        self.testindexer.index_with_lines("text2.txt")
        self.testindexer.index_with_lines("text.txt")
        testsearch = search_engine.SearchEngine('database')
        # context '3,3'
        windowsdict = testsearch.several_tokens_search_with_customizable_context("only kittens", 3, 3)
        expectedwindowresult = {"text.txt": [search_engine.ContextWindow("There are only fluffy kittens",
                                    [indexer.Position_with_lines(10, 14, 0), indexer.Position_with_lines(22, 29, 0)],
                                     search_engine.WindowPosition(0, 29, 0, "text.txt"))],
                                "text2.txt": [search_engine.ContextWindow("only kittens and puppies",
                                    [indexer.Position_with_lines(0, 4, 0), indexer.Position_with_lines(5, 12, 0)],
                                     search_engine.WindowPosition(0, 24, 0, "text2.txt"))]}
        self.assertEqual(expectedwindowresult, windowsdict)
        
    def test_context_window_search_sentence_extension(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only fluffy kittens! Only kittens")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        
        testsearch = search_engine.SearchEngine('database')
        
        windowsdict = testsearch.several_tokens_search_with_sentence_context("only", 0, 0)
        expectedwindowresult = {"text.txt": [search_engine.ContextWindow("There are only fluffy kittens! Only kittens",
                                    [indexer.Position_with_lines(10, 14, 0)],
                                     search_engine.WindowPosition(0, 30, 0, "text.txt"))]}
        self.assertEqual(windowsdict, expectedwindowresult)
            
        windowsdict = testsearch.several_tokens_search_with_sentence_context("only fluffy", 3, 3)
        expectedwindowresult = {"text.txt": [search_engine.ContextWindow("There are only fluffy kittens! Only kittens",
                                    [indexer.Position_with_lines(10, 14, 0), indexer.Position_with_lines(15, 21, 0)],
                                     search_engine.WindowPosition(0, 43, 0, "text.txt"))]}
        self.assertEqual(windowsdict, expectedwindowresult)
            
        windowsdict = testsearch.several_tokens_search_with_sentence_context("kittens", 1, 1)
        expectedwindowresult = {"text.txt": [search_engine.ContextWindow("There are only fluffy kittens! Only kittens",
                                    [indexer.Position_with_lines(22, 29, 0), indexer.Position_with_lines(36, 43, 0)],
                                     search_engine.WindowPosition(0, 43, 0, "text.txt"))]}
        self.assertEqual(windowsdict, expectedwindowresult)

    def test_context_window_highlighted_search(self):
        testfile = open("text.txt", 'w')
        testfile.write("There are only fluffy kittens! Only kittens")
        testfile.close()
        self.testindexer.index_with_lines("text.txt")
        testfile2 = open("text2.txt", 'w')
        testfile2.write("only kittens and puppies...")
        testfile2.close()
        self.testindexer.index_with_lines("text2.txt")
        testsearch = search_engine.SearchEngine('database')
        
        windowsdict = testsearch.highlighted_context_window_search("only", 1, 1)
        expectedwindowresult = {"text.txt": ["There are <B>only</B> fluffy kittens!"],
                                "text2.txt": ["<B>only</B> kittens and puppies..."]}
        self.assertEqual(windowsdict, expectedwindowresult)
            
        windowsdict = testsearch.highlighted_context_window_search("only fluffy", 3, 3)
        expectedwindowresult = {"text.txt": ["There are <B>only</B> <B>fluffy</B> kittens! Only kittens"]}
        self.assertEqual(windowsdict, expectedwindowresult)
            
        windowsdict = testsearch.highlighted_context_window_search("kittens", 1, 1)
        expectedwindowresult = {"text.txt": ["There are only fluffy <B>kittens</B>! Only <B>kittens</B>"],
                                "text2.txt": ["only <B>kittens</B> and puppies..."]}
        self.assertEqual(windowsdict, expectedwindowresult)

    def tearDown(self):
        self.testindexer.closeDatabase()
        for filename in os.listdir(os.getcwd()):
            if (filename == "database" or filename.startswith('database.')):
                os.remove(filename)
            if (filename == "text" or filename.startswith('text')):
                os.remove(filename)

if __name__=='__main__':
    unittest.main() 
