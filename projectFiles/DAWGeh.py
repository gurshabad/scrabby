import sys, time
class DawgNode:
	NextID = 0

	def __init__(self):
		self.id = DawgNode.NextID
		DawgNode.NextID += 1
		self.final = False
		self.edges = {}

	def __str__(self):
		arr = []
		if self.final:
			arr.append('1')
		else:
			arr.append('0')

		for (label, node) in self.edges.iteritems():
			arr.append(label)
			arr.append(str(node.id))

		return "_".join(arr)

	def __hash__(self):
		return self.__str__().__hash__()

	def __eq__(self, other):
		return self.__str__() == other.__str__()

class Dawg:
	def __init__(self):
		self.previousWord = ""
		self.root = DawgNode()

		self.uncheckedNodes = []
		self.minimizedNodes = {}

	def insert(self, word):
		if(word < self.previousWord):
			raise Exception("ERROR! WORD not alpha order PREV_WORD")

		commonPrefix = 0

		for i in range(min(len(word), len(self.previousWord))):
			if ( word[i] != self.previousWord[i]): break
			commonPrefix += 1

		self._minimize(commonPrefix)

		if (len(self.uncheckedNodes) == 0):
			node = self.root
		else:
			node = self.uncheckedNodes[-1][2]

		for letter in word[commonPrefix:]:
			nextNode = DawgNode()
			node.edges[letter] = nextNode
			self.uncheckedNodes.append((node, letter, nextNode))
			node = nextNode

		node.final = True
		self.previousWord = word

	def finish(self):
		self._minimize(0)

	def _minimize(self, downTo):
		for i in range(len(self.uncheckedNodes) - 1, downTo - 1, -1):
			(parent, letter, child) = self.uncheckedNodes[i]
			if child in self.minimizedNodes:
				parent.edges[letter] = self.minimizedNodes[child]
			else:
				self.minimizedNodes[child] = child
			self.uncheckedNodes.pop()

	def lookup(self, word):
		node = self.root
		for letter in word:
			if letter not in node.edges: return False
			node = node.edges[letter]

		return node.final

	def nodeCount(self):
		return len(self.minimizedNodes)

	def edgeCount(self):
		count = 0
		for node in self.minimizedNodes:
			count += len(node.edges)
		return count

dawg = Dawg()
WordCount = 0
words = open(sys.argv[1], 'rt').read().split()
words.sort()
start = time.time()
for word in words:
	WordCount += 1
	dawg.insert(word)
dawg.finish()
print "Dawg creation took %g s" % (time.time() - start)
frontier = [dawg.root]

def traverse(edges, uptillnow):
	# print edges
	if(len(edges)):
		for _ in edges:
			if(edges[_].final == True):
				print uptillnow+_
				traverse(edges[_].edges, uptillnow+_)

traverse(dawg.root.edges, "")
print dawg.lookup("catni")
# while(len(frontier)):
# 	print frontier[0].edges
# 	for _ in frontier[0].edges:
# 		frontier.append(frontier[0].edges[_])
# 	frontier = frontier[1:]
