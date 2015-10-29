class Tile:
	letter = '_'
	value = -1

	def __init__(self, l = '_'):
		self.letter = l
		self.value = self.getVal(l)

	def getVal(self):
		return self.value

	def getVal(self, l):
		if l in "_": return -1
		if l in " ": return 0
		if l in "AEILNORSTU": return 1
		if l in "DG": return 2
		if l in "BCMP": return 3
		if l in "FHVWY": return 4
		if l in "K": return 5
		if l in "JX": return 8
		if l in "QZ": return 10