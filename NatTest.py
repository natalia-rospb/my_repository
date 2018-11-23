import unittest
import tokenizer_natashka_final

class TokenizerTest(unittest.TestCase):
    def setUp(self):
        self.t = tokenizer_natashka_final.Tokenizator()
    
    def test_tokens_collection_is_list(self):
        self.assertIsInstance(self.t.tokenize('Мама мыла раму'),list)

    def test_token_type_in_list(self):
        tokenscollection = self.t.tokenize('Мама мыла раму')
        self.assertIsInstance(tokenscollection[0],tokenizer_natashka_final.Token)

    def test_input_type_int(self):
        s = 1414
        with self.assertRaises(TypeError):
            tokenscollection = self.t.tokenize(s)
            
    def test_input_type_float(self):
        v = 0.427
        with self.assertRaises(TypeError):
            tokenscollection2 = self.t.tokenize(v)

    def test_tokenizer_token_position(self):
        tokenscollection = list(self.t.tokenize('This is my sentence.'))
        self.assertEqual(len(tokenscollection),4)
        self.assertEqual(tokenscollection[0].position, 0)
        self.assertEqual(tokenscollection[1].position, 5)
        self.assertEqual(tokenscollection[2].position, 8)
        self.assertEqual(tokenscollection[3].position, 11)

    def test_tokenizer_punctuation_in_the_end(self):
        tokenscollection = list(self.t.tokenize('This is my sentence.'))
        self.assertEqual(len(tokenscollection),4)
        self.assertEqual(tokenscollection[0].word, 'This')
        self.assertEqual(tokenscollection[1].word, 'is')
        self.assertEqual(tokenscollection[2].word, 'my')
        self.assertEqual(tokenscollection[3].word, 'sentence')
        
    def test_tokenizer_punctuation_in_the_beginning(self):
        tokenscollection = list(self.t.tokenize('.This is my sentence'))
        self.assertEqual(len(tokenscollection),4)
        self.assertEqual(tokenscollection[0].word, 'This')
        self.assertEqual(tokenscollection[1].word, 'is')
        self.assertEqual(tokenscollection[2].word, 'my')
        self.assertEqual(tokenscollection[3].word, 'sentence')

    def test_tokenizer_russian_punctuation_in_the_end(self):
        tokenscollection = list(self.t.tokenize('Это мое предложение.'))
        self.assertEqual(len(tokenscollection),3)
        self.assertEqual(tokenscollection[0].word, 'Это')
        self.assertEqual(tokenscollection[1].word, 'мое')
        self.assertEqual(tokenscollection[2].word, 'предложение')
        
    def test_tokenizer_sentence_of_spaces(self):
        tokenscollection = list(self.t.tokenize('   '))
        self.assertEqual(len(tokenscollection),0)       
        self.assertEqual(tokenscollection, [])


class _GetTypeTest(unittest.TestCase):
    
    def setUp(self):
        self.t = tokenizer_natashka_final.Tokenizator()
        
    def test_token_type(self):
        typeinquestion = self.t._getType("1")
        self.assertEqual(typeinquestion, "d")
        typeinquestion = self.t._getType("v")
        self.assertEqual(typeinquestion, "a")
        typeinquestion = self.t._getType("Щ")
        self.assertEqual(typeinquestion, "a")
        typeinquestion = self.t._getType(")")
        self.assertEqual(typeinquestion, "p")
        typeinquestion = self.t._getType(" ")
        self.assertEqual(typeinquestion, "s")
        typeinquestion = self.t._getType("+")
        self.assertEqual(typeinquestion, "o")
        typeinquestion = self.t._getType("\n")
        self.assertEqual(typeinquestion, "o")


class GeneratorTest(unittest.TestCase):
    
    def setUp(self):
        self.t = tokenizer_natashka_final.Tokenizator()
        
    def test_tokenscollection_is_list(self):
        self.assertIsInstance(list(self.t.generate('Мама мыла раму')),list)

    def test_generator_english(self):
        tokenscollection = list(self.t.generate('Everything is good!!*4+'))
        self.assertEqual(len(tokenscollection),3)
        self.assertEqual(tokenscollection[0].word, 'Everything')
        self.assertEqual(tokenscollection[0].position, 0)
        self.assertEqual(tokenscollection[1].word, 'is')
        self.assertEqual(tokenscollection[1].position, 11)
        self.assertEqual(tokenscollection[2].word, 'good')

    def test_generator_russian(self):
        tokenscollection = list(self.t.generate('  Всё хорошо! 537))*!'))
        self.assertEqual(len(tokenscollection),2)
        self.assertEqual(tokenscollection[0].word, 'Всё')
        self.assertEqual(tokenscollection[0].position, 2)
        self.assertEqual(tokenscollection[1].word, 'хорошо')
        self.assertEqual(tokenscollection[1].position, 6)

    def test_generator_punctuation_in_the_beginning(self):
        tokenscollection = list(self.t.generate('.This is my sentence'))
        self.assertEqual(len(tokenscollection),4)
        self.assertEqual(tokenscollection[0].word, 'This')
        self.assertEqual(tokenscollection[1].word, 'is')
        self.assertEqual(tokenscollection[2].word, 'my')
        self.assertEqual(tokenscollection[3].word, 'sentence')

    def test_generator_punctuation_in_the_end(self):
        tokenscollection = list(self.t.generate('This is my sentence.'))
        self.assertEqual(len(tokenscollection),4)
        self.assertEqual(tokenscollection[0].word, 'This')
        self.assertEqual(tokenscollection[1].word, 'is')
        self.assertEqual(tokenscollection[2].word, 'my')
        self.assertEqual(tokenscollection[3].word, 'sentence')
        
    def test_generator_sentence_of_spaces(self):
        tokenscollection = list(self.t.generate('   '))
        self.assertEqual(len(tokenscollection),0)        
        self.assertEqual(tokenscollection, [])
        
    def test_generator_empty_sentence(self):
        tokenscollection = list(self.t.generate(''))
        self.assertEqual(len(tokenscollection),0)
        self.assertEqual(tokenscollection, [])


class GenerateWithTypesTest(unittest.TestCase):
    
    def setUp(self):
        self.t = tokenizer_natashka_final.Tokenizator()

    def test_tokenscollection_is_list(self):
        self.assertIsInstance(list(self.t.generate_with_types('Мама мыла раму')),list)
        
    def test_generator_english(self):
        tokenscollection = list(self.t.generate_with_types('Everything is good!!*4+'))
        self.assertEqual(tokenscollection[0].word, 'Everything')
        self.assertEqual(tokenscollection[0].position, 0)
        self.assertEqual(tokenscollection[0].typ, 'a')
        self.assertEqual(tokenscollection[1].word, ' ')
        self.assertEqual(tokenscollection[1].position, 10)
        self.assertEqual(tokenscollection[1].typ, 's')
        self.assertEqual(tokenscollection[4].word, 'good')
        self.assertEqual(tokenscollection[4].position, 14)
        self.assertEqual(tokenscollection[4].typ, 'a')
        self.assertEqual(tokenscollection[5].word, '!!*')
        self.assertEqual(tokenscollection[5].position, 18)
        self.assertEqual(tokenscollection[5].typ, 'p')
        self.assertEqual(tokenscollection[6].word, '4')
        self.assertEqual(tokenscollection[6].position, 21)
        self.assertEqual(tokenscollection[6].typ, 'd')
        self.assertEqual(tokenscollection[7].word, '+')
        self.assertEqual(tokenscollection[7].position, 22)
        self.assertEqual(tokenscollection[7].typ, 'o')
        
    def test_generator_russian(self):
        tokenscollection = list(self.t.generate_with_types('  Всё хорошо! 537))*!'))
        self.assertEqual(tokenscollection[0].word, '  ')
        self.assertEqual(tokenscollection[0].position, 0)
        self.assertEqual(tokenscollection[0].typ, 's')
        self.assertEqual(tokenscollection[1].word, 'Всё')
        self.assertEqual(tokenscollection[1].position, 2)
        self.assertEqual(tokenscollection[1].typ, 'a')
        self.assertEqual(tokenscollection[3].word, 'хорошо')
        self.assertEqual(tokenscollection[3].position, 6)
        self.assertEqual(tokenscollection[3].typ, 'a')
        self.assertEqual(tokenscollection[4].word, '!')
        self.assertEqual(tokenscollection[4].position, 12)
        self.assertEqual(tokenscollection[4].typ, 'p')
        self.assertEqual(tokenscollection[6].word, '537')
        self.assertEqual(tokenscollection[6].position, 14)
        self.assertEqual(tokenscollection[6].typ, 'd')
        self.assertEqual(tokenscollection[7].word, '))*!')
        self.assertEqual(tokenscollection[7].position, 17)
        self.assertEqual(tokenscollection[7].typ, 'p')

    def test_generator_punctuation_in_the_beginning(self):
        tokenscollection = list(self.t.generate_with_types('.This is my sentence'))
        self.assertEqual(len(tokenscollection),8)
        self.assertEqual(tokenscollection[0].word, '.')
        self.assertEqual(tokenscollection[1].word, 'This')
        self.assertEqual(tokenscollection[2].word, ' ')
        self.assertEqual(tokenscollection[3].word, 'is')
        self.assertEqual(tokenscollection[4].word, ' ')
        self.assertEqual(tokenscollection[5].word, 'my')
        self.assertEqual(tokenscollection[6].word, ' ')
        self.assertEqual(tokenscollection[7].word, 'sentence')

    def test_generator_punctuation_in_the_end(self):
        tokenscollection = list(self.t.generate_with_types('This is my sentence.'))
        self.assertEqual(len(tokenscollection),8)
        self.assertEqual(tokenscollection[0].word, 'This')
        self.assertEqual(tokenscollection[1].word, ' ')
        self.assertEqual(tokenscollection[2].word, 'is')
        self.assertEqual(tokenscollection[3].word, ' ')
        self.assertEqual(tokenscollection[4].word, 'my')
        self.assertEqual(tokenscollection[5].word, ' ')
        self.assertEqual(tokenscollection[6].word, 'sentence')
        self.assertEqual(tokenscollection[7].word, '.')
        
    def test_generator_sentence_of_spaces(self):
        tokenscollection = list(self.t.generate_with_types('   '))
        self.assertEqual(len(tokenscollection),1)
        self.assertEqual(tokenscollection[0].word, '   ')
        self.assertEqual(tokenscollection[0].position, 0)
        self.assertEqual(tokenscollection[0].typ, 's')        

    def test_generator_empty_sentence(self):
        tokenscollection = list(self.t.generate_with_types(''))
        self.assertEqual(len(tokenscollection),0)
        self.assertEqual(tokenscollection, [])
        
if __name__ == '__main__':
    unittest.main()

