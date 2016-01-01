import tile

class Square:

	#tile = Tile() # The tile that is on the square
	#occupied = False # Whether the square is occupied or not
	#isAnchor = False # Whether the square is an anchor square or not
	#crossCheck = [] # Something that Anmol needed
	""" 1 - Nothing Special, 2 - Double Letter(DL), 3 - Triple Letter(TL), 4 - Double Word(DW), 5 - Triple Word(TW) """
	#letterMultiplier = 1 # Double Letter, Triple Letter
	#wordMultiplier = 1 # Double Word, Triple Word

	def __init__(self):
		self.occupied = False
		self.isAnchor = False
		self.downCrossCheck = []
		self.acrossCrossCheck = []
		self.downCrossSum = 0
		self.acrossCrossSum = 0
		
		for _ in range(26):
			self.downCrossCheck.append(True) #If true for a letter, then it is safe to play that letter on this square in a down move.
		self.downCrossCheck.append(False) #To avoid playing the special trie EOW character '{' 
		for _ in range(26):
			self.acrossCrossCheck.append(True) #If true for a letter, then it is safe to play that letter on this square in an across move.
		self.acrossCrossCheck.append(False) #To avoid playing the special trie EOW character '{' 

		self.letterMultiplier = 1
		self.wordMultiplier = 1
		self.tile = tile.Tile()

	def changeLSpeciality(self,val): # Change the letter multiplier type of the square
		self.letterMultiplier = val

	def changeWSpeciality(self,val): # Change the word multiplier type of the square
		self.wordMultiplier = val

	def setTile(self,val): # Place a tile on the square
		self.tile = val
		self.occupied = True

	def setTileVal(self, val):
		self.tile = val

	def getChar(self):
		return self.tile.letter
