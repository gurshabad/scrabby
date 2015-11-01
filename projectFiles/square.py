from tile import *

class Square:

	#tile = Tile() # The tile that is on the square
	#occupied = False # Whether the square is occupied or not
	#isAnchor = False # Whether the square is an anchor square or not
	#crossSet = [] # Something that Anmol needed
	""" 0 - Nothing Special, 1 - Double Letter(DL), 2 - Triple Letter(TL), 3 - Double Word(DW), 4 - Triple Word(TW) """
	#special = 0 # The type of square it is

	def __init__(self):
		self.occupied = False
		self.isAnchor = False
		self.crossSet = []
		for _ in range(26):
			self.crossSet += [False]
		self.special = 0
		self.tile = Tile()

	def changeSpeciality(self,val): # Change the type of the square
		self.special = val

	def setTile(self,val): # Place a tile on the square
		self.tile = val
		self.occupied = True

	def getChar(self):
		return self.tile.letter



def main():
	pass

if __name__ == '__main__':
	main()