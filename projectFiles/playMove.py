from gen_board import *
from tile import *
from copy import deepcopy

def playMove(board, word, pos, isAcross):
	word = word.upper()
	if(isAcross):
		if(14 - (pos[1] + len(word)) < 0):
			print "Length Exceeded.\n\n"
			return board
		for loc, letter in enumerate(word):
			if(board.board[pos[0]][pos[1]+loc].occupied and board.board[pos[0]][pos[1]+loc].getChar() != letter):
				print "Invalid move.\n\n"
				return board
		for loc, letter in enumerate(word):
			board.board[pos[0]][pos[1]+loc].setTile(Tile(letter))
	else:
		if(14 - (pos[0] + len(word)) < 0):
			print "Length Exceeded.\n\n"
			return board
		for loc, letter in enumerate(word):
			if(board.board[pos[0]+loc][pos[1]].occupied and board.board[pos[0]+loc][pos[1]].getChar() != letter):
				print "Invalid move.\n\n"
				return board
		for loc, letter in enumerate(word):
			board.board[pos[0]+loc][pos[1]].setTile(Tile(letter))


def main():
	ourBoard = TheBoard()
	playMove(ourBoard,"hello",(7,7),True)
	ourBoard.printBoard()
	playMove(ourBoard,"close",(6,9),False)
	ourBoard.printBoard()
	playMove(ourBoard,"dayum",(6,11),False)
	ourBoard.printBoard()


if __name__ == '__main__':
	main()