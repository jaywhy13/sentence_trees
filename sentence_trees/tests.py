from django.db import IntegrityError
from django.test import TestCase

from sentence_trees import SentenceTree

class SentenceTest(TestCase):

    def test_sentences(self):
    	sentences = [
	    	"The boy jumped over the fence",
	    	"The boy jumped over the moon",
	    	"The boy jumped under the fence",
	    	"The boy jumped into the car",
	    	"The girl did nothing about the problem",
	    	"The girl phoned home"
    	]

    	sentence_tree = SentenceTree()
    	for sentence in sentences:
            words = sentence.split()
            node = sentence_tree.add_sentence(words)
            self.assertEquals(node.depth-1, len(words))

    	tree_sentences = sentence_tree.get_sentences()

    	self.assertEquals(len(tree_sentences), len(sentences))

    	for tree_sentence in tree_sentences:
    		self.assertIn(" ".join(tree_sentence), sentences)

    	# test word subsets
    	prefixes = ["The girl", "The boy", "The boy jumped", "The girl phoned"]
    	for prefix in prefixes:
    		self.assertTrue(sentence_tree.sentence_in_tree(prefix))


    	# test word completions
    	self.assertEquals(sentence_tree.get_words_after("The"), ["boy", "girl"])
    	self.assertEquals(sentence_tree.get_words_after("The boy"), ["jumped"])
    	self.assertEquals(sentence_tree.get_words_after("The girl"), ["did", "phoned"])

        # test search 
        results = [ node.sentence for node in sentence_tree.search("home") ]
        self.assertIn("The girl phoned home".split(), results)

        # test soundex
        results = [ node.sentence for node in sentence_tree.search("hoome") ]
        self.assertIn("The girl phoned home".split(), results)


