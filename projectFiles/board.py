from pprint import pprint
from termcolor import cprint, colored
import square

class TheBoard:
	"""The Scrabble Board Class"""
	i = 15
	j = 15
	#board = []
	col_index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
	row_index = range(15)

	def __init__(self):
		""" 1 - Nothing Special, 2 - Double Letter(DL), 3 - Triple Letter(TL), 4 - Double Word(DW), 5 - Triple Word(TW) """
		
		self.board = []
		for rows in range(self.i):
			self.board.append([])
			for cols in range(self.j):
				self.board[rows].append(square.Square())

		TW = [(0,0), (0,7), (0,14), (7,0), (7,14), (14,0), (14,7), (14,14)]
		DW = [(1,1), (1,13), (2,2), (2,12), (3,3), (3,11), (4,4), (4,10), (7,7), (10,4), (10,10), (11,3), (11,11), (12,2), (12,12), (13,1), (13,13)]
		TL = [(1,5), (1,9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5), (9,9), (9,13), (13,5), (13,9)]
		DL = [(0,3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (14,3), (14,11), (12,6), (12,8), (11,0), (11,7), (11,14), (6,2), (6,6), (6,8), (6,12), (8,2), (8,6), (8,8), (8,12), (7,3), (7,11)]

		for pair in DL:
			self.board[pair[0]][pair[1]].changeLSpeciality(2)

		for pair in TL:
			self.board[pair[0]][pair[1]].changeLSpeciality(3)

		for pair in DW:
			self.board[pair[0]][pair[1]].changeWSpeciality(2)

		for pair in TW:
			self.board[pair[0]][pair[1]].changeWSpeciality(3)

	def copyBoard(self, obj):
		self.board = obj.board

	def printBoard(self):
		print "\n\n    ",
		for i in self.col_index: print colored( " "+i+" ", 'white', 'on_red', attrs=['bold']),
		print "\n"
		c = 1
		for row in self.board:
			if(c < 10): print colored( "  "+str(c)+" ", 'white', 'on_green', attrs=['bold']),
			else: print colored( " "+str(c)+" ", 'white', 'on_green', attrs=['bold']),
			for entry in row:
				if entry.occupied == True: print colored( " "+entry.tile.letter.upper()+" ", 'grey', 'on_white', attrs=['bold']),
				else:
					if entry.wordMultiplier == 3: print colored('3xW', 'red', attrs=[]),
					elif entry.wordMultiplier == 2: print colored('2xW', 'magenta', attrs=[]),
					elif entry.letterMultiplier == 3: print colored('3xL', 'blue', attrs=[]),
					elif entry.letterMultiplier == 2: print colored('2xL', 'cyan', attrs=[]),
					else: print '___', 
			print "\n"
			c += 1
		print ""
