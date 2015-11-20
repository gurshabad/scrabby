#List of conventions

# All lowercase letters in backend
# 0-indexing

#List ends

from gen_board import *
from tile import *
from rack import *
from trie import *
from copy import deepcopy

#For benchmarking:

def memory_usage():
    """Memory usage of the current process in kilobytes."""
    status = None
    result = {'peak': 0, 'rss': 0}
    try:
        # This will only work on systems with a /proc file system
        # (like Linux).
        status = open('/proc/self/status')
        for line in status:
            parts = line.split()
            key = parts[0][2:-1].lower()
            if key in result:
                result[key] = int(parts[1])
    finally:
        if status is not None:
            status.close()
    return result


def validityCheck(isAcross, board, pos, word, playerRack):

	print isAcross, pos, word

	r = pos[1]
	c = pos[0]

	if(isAcross):
		if(c+len(word) > 15): return False

	else:
		if(r+len(word) > 15): return False

	word = word.lower()
	#print word

	if(isAcross):
		current = [ board.board[r][c+elem].getChar() for elem in range(len(word)) ]
	else:
		current = [ board.board[r+elem][c].getChar() for elem in range(len(word)) ]

	print current

	current = [ i.lower() for i in current ]

	valid = True

	rackCopy = [ t.letter for t in playerRack.rack ]
	deleteThis = []

	for idx, letter in enumerate(word):
		if(letter != current[idx]):
			if (letter not in rackCopy):
				print "Uh oh. Invalid move."
				valid = False
				return False
			else:
				rackCopy.remove(letter)
				deleteThis.append(letter)

	# if not valid:
		# return False

	# else:
	# 	for letter in word:
	# 		if letter not in current:

	# 			tiles = [t.letter for t in playerRack.rack]

	# 			for idx, elem in enumerate(tiles):
	# 				if(tiles[idx] == letter):
	# 					deleteThis.append(letter)
	# 					#playerRack.removeTile(idx)
	# 					break

	return ''.join(deleteThis).upper()



def playerMove(board, word, pos, isAcross):

	if(isAcross):
		if(15 - (pos[0] + len(word)) < 0):
			print "Length Exceeded.\n\n"
			return False
		for loc, letter in enumerate(word):
			if(board.board[pos[1]][pos[0]+loc].occupied and board.board[pos[1]][pos[0]+loc].getChar() != letter):
				print "Invalid move.\n\n"
				return False

		if not pos[0] == 0:
			board.board[pos[1]][pos[0]-1].isAnchor = True;
		if not pos[0] + len(word)-1 == 14:
			board.board[pos[1]][pos[0]+len(word)].isAnchor = True;

		for loc, letter in enumerate(word):
			if not pos[1] == 14:
				board.board[pos[1]+1][pos[0]+loc].isAnchor = True;
			if not pos[1] == 0:
				board.board[pos[1]-1][pos[0]+loc].isAnchor = True;
			board.board[pos[1]][pos[0]+loc].setTile(Tile(letter))

	else:
		if(15 - (pos[1] + len(word)) < 0):
			print "Length Exceeded.\n\n"
			return False
		for loc, letter in enumerate(word):
			if(board.board[pos[1]+loc][pos[0]].occupied and board.board[pos[1]+loc][pos[0]].getChar() != letter):
				print "Invalid move.\n\n"
				return False

		if not pos[1] == 0:
			board.board[pos[1]-1][pos[0]].isAnchor = True;
		if not pos[1] + len(word)-1 == 14:
			board.board[pos[1]+len(word)][pos[0]].isAnchor = True;

		for loc, letter in enumerate(word):
			if not pos[0] == 14:
				board.board[pos[1]+loc][pos[0] + 1].isAnchor = True;
			if not pos[0] == 0:
				board.board[pos[1]+loc][pos[0]-1].isAnchor = True;

			board.board[pos[1]+loc][pos[0]].setTile(Tile(letter))


import string, random
import datetime

#Backbone DAWG move generator for Scrabby
#Trie construction of the word list begins

trieStart = datetime.datetime.now()

wordListTrie = Trie()

inputFile = open('Lexicon.txt','r')

for word in inputFile:

	dontAdd = False

	#Check if input is sanitized
	#Don't allow anything other than lowercase English letters and EOW({)
	for item in word.strip():
		if(ord(item) > 123 or ord(item) < 97):
			dontAdd = True
	#If everything is okay		
	if not dontAdd:
		wordListTrie.addWord(word.strip())

trieEnd = datetime.datetime.now()

#Trie construction time
#print (trieEnd - trieStart).microseconds

#Trie construction done

###########
#TO-DO: Construct DAWG from Trie
###########

############## TESTING AREA #####################

############# TESTING AREA ENDS ##################

#TO-DO#####
#Implementation of cross check sets and anchor squares.
###########

#Implementation of back-tracking algorithms presented in the paper 'The World's Fastest Scrabble Program' by Appel and Jacobson
#https://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf
#Modified to handle more edge cases


#Note on the leftPart function:
#'limit' is the no of contiguous non anchor squares to the left of current anchorSquare
#leftPart creates all possible proper prefixes, to the left of the anchorSquare under consideration
#if some prefix is not present already. It is bounded by 'limit'.
#
#For extendRightBeta: For each prefix formed, it tries to place playable characters on anchorSquare
#by calling extendRightBeta

anchorSquare = 0

def leftPart(board, rowIdx, rack, partialWord, currentNode, limit):

	#Case 1: Left of anchor square occupied
	if(board[rowIdx][anchorSquare-1].getChar() != '_'):
		leftSquare = anchorSquare-1
		leftBit = board[rowIdx][leftSquare].getChar()

		#Construct the existing leftPart
		while(board[rowIdx][leftSquare-1].getChar() != '_'):
			leftSquare = leftSquare - 1
			leftBit = board[rowIdx][leftSquare].getChar() + leftBit

		#Walk down the trie to node with leftBit path
		for element in leftBit:
			currentNode = currentNode.children[element]

		#For each tile playable on anchorSquare
		for child in currentNode.children:
			if child in rack:
				extendRightBeta(board, rowIdx, rack, leftBit + child, currentNode.children[child], anchorSquare)

	#Case 2: Left of anchor square vacant
	else:

		#For each tile playable on anchorSquare
		for child in currentNode.children:
			if child in rack:
				extendRightBeta(board, rowIdx, rack, partialWord + child, currentNode.children[child], anchorSquare)

		if limit > 0:
			for child in currentNode.children:
				if child in rack:
					rack.remove(child)
					leftPart( board, rowIdx, rack, partialWord + child, currentNode.children[child], limit-1)
					rack.append(child)


legalWords = []

#extendRightBeta notes-
#The below function considers the situation at each step where:
#partialWord[:-1](partialWord without last letter) is already on the board
#We are looking to add currentNode to the end of partialWord[:-1]
#The validity of placing currentNode has already been checked (partialWord is some valid prefix)

def extendRightBeta(board, rowIdx, rack, partialWord, currentNode, square):

	#Case 1: At the board's edge. Play currentNode and check validity of partialWord.
	if(square == 14):
		if '{' in currentNode.children:
			legalWords.append((partialWord, square))

	#Case 2: Still looking to place more tiles on the board after this move if we can
	else:
		#Case 2.1: If square next to where we want to place letter on currentNode on is empty.
		if(board[rowIdx][square+1].getChar() == '_'): 

			#Play and check if partial word is legal.   
			if '{' in currentNode.children:
				legalWords.append((partialWord, square))

			#Find a candidate tile to play at the next square and call extendRight on it
			for child in currentNode.children:
				if child in rack:  #and it can be legally placed on the next square.
					rack.remove(child)
					extendRightBeta(board, rowIdx, rack,partialWord + child, currentNode.children[child], square + 1)
					rack.append(child)

		#Case 2.2: If square next to where we want to place letter from currentNode on is full. Hey, no worries!
		#Just check if playing the occupying letter after currentNode will give us some valid prefix 
		else:
			if board[rowIdx][square+1].getChar() in currentNode.children:
				extendRightBeta(board, rowIdx, rack, partialWord + board[rowIdx][square+1].getChar(), currentNode.children[board[rowIdx][square+1].getChar()], square + 1)


# anchorSquare = 2
# limit = 6
# limit = min(limit, anchorSquare)

# findStart = datetime.datetime.now()

# leftPart('', newTrie.root, limit)

# #legalWords = list(set(legalWords))

# findEnd = datetime.datetime.now()

# #Time to generate all moves for one row
# #print (findEnd - findStart).microseconds

# print sorted(legalWords)

# for word in legalWords:
# 	if(newTrie.query(word[0]) == False):
# 		print "Shit, ", word[0]

allLetters = "eeeeeeeeeeeeaaaaaaaaaiiiiiiiiioooooooonnnnnnrrrrrrttttttllllssssuuuuddddgggbbccmmppffhhvvwwyykjxqz"

occupiedMatrix = [[0] * 15] * 15

def getClashes(r, c, word, occupiedMatrix):
    for i in range(len(word)):
        up = r
        down = r
        if ((r - 1 < 15) and (r - 1 >= 0) and (c+i < 15) and (c+i >=0)):
            if occupiedMatrix[r-1][c+i] == 1:
                up = r - 1
                while up > 0:
                    if occupiedMatrix[up][c+i] == 1:
                        up = up - 1

        if ((r + 1 < 15) and (r + 1 >= 0) and (c+i < 15) and (c+i >= 0)):
            if occupiedMatrix[r+1][c+i] == 1:
                down = r + 1
                while down < 15:
                    if occupiedMatrix[down][c+i] == 1:
                        down = down - 1

        #form word, wordListTrie.query(word)


# def main():

# 	ourBoard = TheBoard()
# 	ourBoard.printBoard()

# 	playerRack = Rack()
# 	computerRack = Rack()

# 	bag = [ letter for letter in allLetters ]

# 	bag = playerRack.replenish(bag);
# 	bag = computerRack.replenish(bag);

# 	playerTurn = True
# 	print "You get to move first! Here is your rack"

# 	while(len(bag)):

# 		bag = playerRack.replenish(bag);
# 		playerRack.showRack()

# 		while(playerTurn):

# 			#User input.

# 			print "Enter number of tiles you wanna play:"
# 			wordLength = input()
# 			print "Enter word:"
# 			word = raw_input()
# 			if not wordListTrie.query(word):
# 				print "\nSorry, not a word. Try again.\n"
# 				continue

# 			print "Enter 'True' if across else 'False':"
# 			isAcross = raw_input()
# 			if(isAcross == 'True' or isAcross == 'true'):
# 				isAcross = True
# 			else:
# 				isAcross = False

# 			print "Enter 0-indexed start position(r c):"
# 			start = map(int, raw_input().split())
# 			r,c = start[0],start[1]

# 			#Validity checking.
# 			if(isAcross):
# 				current = [ ourBoard.board[r][c+elem].getChar() for elem in range(len(word)) ]
# 			else:
# 				current = [ ourBoard.board[r+elem][c].getChar() for elem in range(len(word)) ]

# 			valid = True
# 			for letter in word:
# 				if (letter not in current) and (letter not in [ t.letter for t in playerRack.rack ]):
# 					print "Uh oh. Invalid move."
# 					playerTurn = True 
# 					valid = False
# 					break

# 			if not valid:
# 				continue
# 			else:
# 				for letter in word:
# 					if letter not in current:

# 						tiles = [t.letter for t in playerRack.rack]

# 						for idx, elem in enumerate(tiles):
# 							if(tiles[idx] == letter):
# 								playerRack.removeTile(idx)
# 								break

# 				playerMove(ourBoard, word, (c,r), isAcross)
# 				checkClashes(r, c, occupiedMatrix)

# 			playerTurn = False
# 			ourBoard.printBoard()

# 		while(not playerTurn):
# 			#Add AI moves here

# 			computerRack.showRack()

# 			rack = [tile.letter for tile in computerRack.rack]
# 			anchorSquare = 8
# 			leftPart(ourBoard.board, 7, rack, '', wordListTrie.root, 7)

# 			print legalWords[0]
# 			playerMove(ourBoard,legalWords[0][0], (7,7), isAcross)

# 			# for rowIdx, row in enumerate(ourBoard.board):
# 			# 	flag = False
# 			# 	for idx, sq in enumerate(row):
# 			# 		prevAnchor = -1
# 			# 		if sq.isAnchor:

# 			# 			rack = [tile.letter for tile in computerRack.rack]
# 			# 			limit = min(idx, idx-prevAnchor-1)
# 			# 			anchorSquare = idx
# 			# 			prevAnchor = anchorSquare
# 			# 			del legalWords[:]
# 			# 			print "Position:", rowIdx, idx
# 			# 			print sorted(legalWords)
# 			# 			#playerMove(ourBoard,legalWords[0], (rowIdx,idx), isAcross)
# 			# 			flag = True
# 			# 			break
# 			# 	if(flag):
# 			# 		break


# 			playerTurn = True
		
# if __name__ == '__main__':
# 	main()
