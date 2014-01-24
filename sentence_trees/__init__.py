import types

from node.base import BaseNode
import fuzzy

soundex = fuzzy.Soundex(4)

class SentenceTreeNode(BaseNode):
	""" A node in the sentence tree represents a word
	"""

	def __init__(self, word):
		super(SentenceTreeNode, self).__init__(word)
		# Keep track of each nodes by their phonetic value
		self.soundex_codes = {}

	@property
	def depth(self):
		d = 0
		node = self
		while node is not None:
			d += 1
			node = node.parent
		return d

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
		return self.subtree_exists(sentence.split())

	def subtree_exists(self, words):
		""" Returns True if the words exist in the tree starting at the root
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
		if not self.subtree_exists(words):
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


	def add_soundex_code(self, word, word_node):
		""" Adds the node's soundex code to a hash to enable very fast searching 
			of the tree
		"""
		code = soundex(word)
		nodes = self.soundex_codes.get(code, [])
		nodes.append(word_node)
		self.soundex_codes[code] = nodes

	def search(self, query):
		""" Allows the user to search the tree for a query
		"""
		nodes = []
		code = soundex(query)
		if code in self.soundex_codes:
			nodes = self.soundex_codes.get(code)
		else:
			words = query.split()
			if len(words) > 1:
				for word in words:
					nodes.extend(self.search(word))
		return nodes


	def add_sentence(self, sentence):
		""" Adds a sentence to the tree and returns the leaf node
		"""
		if type(sentence) == types.StringType:
			sentence = sentence.split()
		parent_node = self
		word_node = None
		for word in sentence:
			last_word = sentence[-1:] == [word]
			if word not in parent_node:
				# add the word to the tree
				word_node = self.create_node(word)
				parent_node[word] = word_node
				parent_node = word_node
				self.add_soundex_code(word, word_node)
			else:
				parent_node = parent_node[word]
		if not word_node:
			return parent_node
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
