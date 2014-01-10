import types

from node.base import BaseNode

class SentenceTreeNode(BaseNode):
	""" A node in the sentence tree represents a word
	"""

	def __init__(self, word):
		super(SentenceTreeNode, self).__init__(word)

	def create_node(self, word):
		""" Creates a new node
		"""
		return SentenceTreeNode(word)

	@property
	def sentence(self):
		return self.path[1:]

	@property
	def sentence_count(self):
		return len(self.get_sentences())

	def sentence_in_tree(self, sentence):
		return self.words_in_tree(sentence.split())

	def words_in_tree(self, words):
		""" Returns True if the words exist in the tree
		"""
		parent_node = self
		for word in words:
			if word in parent_node:
				parent_node = parent_node[word]
			else:
				return False
		return True

	def get_nodes_after(self, words=[]):
		""" Returns a list of possible words after a phrase
		"""
		words = words.split() if type(words) == types.StringType else words
		if not self.words_in_tree(words):
			return []

		nodes = []
		parent_node = self
		for word in words:
			parent_node = parent_node[word]

		for word in parent_node:
			nodes.append(parent_node[word])
		return nodes

	def get_words_after(self, words):
		nodes = self.get_nodes_after(words)
		return [ node.name for node in nodes ]


	def add_sentence(self, sentence):
		""" Adds a sentence to the tree and returns the leaf node
		"""
		parent_node = self
		word_node = None
		for word in sentence:
			if word not in parent_node:
				# add the word to the tree
				word_node = self.create_node(word)
				parent_node[word] = word_node
				parent_node = word_node
			else:
				parent_node = parent_node[word]
		return word_node

	def get_sentences(self):
		sentences = []

		for child in self:
			child_node = self[child]
			if len(child_node) == 0:
				sentences.append(child_node.sentence)
			else:
				child_sentences = child_node.get_sentences()
				for child_sentence in child_sentences:
					if child_sentence:
						sentences.append(child_sentence)
		return sentences

class SentenceTree(SentenceTreeNode):
	""" A sentence tree is simply a tree of words
	"""

	def __init__(self):
		super(SentenceTree, self).__init__("root")
