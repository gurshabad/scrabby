#List of conventions

# All lowercase letters in backend
# 0-indexing

#List ends

from gen_board import *
from tile import *
from rack import *
from trie import *
from copy import deepcopy

def playerMove(board, word, pos, isAcross):

	if(isAcross):
		if(15 - (pos[1] + len(word)) < 0):
			print "Length Exceeded.\n\n"
			return board
		for loc, letter in enumerate(word):
			if(board.board[pos[0]][pos[1]+loc].occupied and board.board[pos[0]][pos[1]+loc].getChar() != letter):
				print "Invalid move.\n\n"
				return board
		for loc, letter in enumerate(word):
			board.board[pos[0]][pos[1]+loc].setTile(Tile(letter))
	else:
		if(15 - (pos[0] + len(word)) < 0):
			print "Length Exceeded.\n\n"
			return board
		for loc, letter in enumerate(word):
			if(board.board[pos[0]+loc][pos[1]].occupied and board.board[pos[0]+loc][pos[1]].getChar() != letter):
				print "Invalid move.\n\n"
				return board
		for loc, letter in enumerate(word):
			board.board[pos[0]+loc][pos[1]].setTile(Tile(letter))


import string, random
import datetime

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

#Backbone DAWG move generator for Scrabby

#Trie construction of the word list begins

trieStart = datetime.datetime.now()

newTrie = Trie()

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
		newTrie.addWord(word.strip())

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

def leftPart(partialWord, currentNode, limit):

	#Case 1: Left of anchor square occupied
	if(board[0][anchorSquare-1] != '_'):
		leftSquare = anchorSquare-1
		leftBit = board[0][leftSquare]

		#Construct the existing leftPart
		while(board[0][leftSquare-1] != '_'):
			leftSquare = leftSquare - 1
			leftBit = board[0][leftSquare] + leftBit

		#Walk down the trie to node with leftBit path
		for element in leftBit:
			currentNode = currentNode.children[element]

		#For each tile playable on anchorSquare
		for child in currentNode.children:
			if child in rack:
				extendRightBeta(leftBit + child, currentNode.children[child], anchorSquare)

	#Case 2: Left of anchor square vacant
	else:

		#For each tile playable on anchorSquare
		for child in currentNode.children:
			if child in rack:
				extendRightBeta(partialWord + child, currentNode.children[child], anchorSquare)

		if limit > 0:
			for child in currentNode.children:
				if child in rack:
					rack.remove(child)
					leftPart(partialWord + child, currentNode.children[child], limit-1)
					rack.append(child)


legalWords = []

#extendRightBeta notes-
#The below function considers the situation at each step where:
#partialWord[:-1](partialWord without last letter) is already on the board
#We are looking to add currentNode to the end of partialWord[:-1]
#The validity of placing currentNode has already been checked (partialWord is some valid prefix)

def extendRightBeta(partialWord, currentNode, square):

	#Case 1: At the board's edge. Play currentNode and check validity of partialWord.
	if(square == 14):
		if '{' in currentNode.children:
			legalWords.append((partialWord, square))

	#Case 2: Still looking to place more tiles on the board after this move if we can
	else:
		#Case 2.1: If square next to where we want to place letter on currentNode on is empty.
		if(board[0][square+1] == '_'): 

			#Play and check if partial word is legal.   
			if '{' in currentNode.children:
				legalWords.append((partialWord, square))

			#Find a candidate tile to play at the next square and call extendRight on it
			for child in currentNode.children:
				if child in rack:  #and it can be legally placed on the next square.
					rack.remove(child)
					extendRightBeta(partialWord + child, currentNode.children[child], square + 1)
					rack.append(child)

		#Case 2.2: If square next to where we want to place letter from currentNode on is full. Hey, no worries!
		#Just check if playing the occupying letter after currentNode will give us some valid prefix 
		else:
			if board[0][square+1] in currentNode.children:
				extendRightBeta(partialWord + board[0][square+1], currentNode.children[board[0][square+1]], square + 1)


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

# mem = memory_usage()
# print "Peak(MB):", mem['peak']/1024.0, ", Current(MB):", mem['rss']/1024.0

# for word in legalWords:
# 	if(newTrie.query(word[0]) == False):
# 		print "Shit, ", word[0]

allLetters = "eeeeeeeeeeeeaaaaaaaaaiiiiiiiiioooooooonnnnnnrrrrrrttttttllllssssuuuuddddgggbbccmmppffhhvvwwyykjxqz"

def main():

	ourBoard = TheBoard()
	ourBoard.printBoard()

	playerRack = Rack()
	computerRack = Rack()

	bag = [ letter for letter in allLetters ]

	bag = playerRack.replenish(bag);
	bag = computerRack.replenish(bag);

	playerTurn = True
	print "You get to move first! Here is your rack"

	while(len(bag)):

		bag = playerRack.replenish(bag);
		playerRack.showRack()

		while(playerTurn):

			print "Enter number of tiles you wanna play:"
			wordLength = input()
			print "Enter word:"
			word = raw_input()
			print "Enter 'True' if across else 'False':"
			isAcross = raw_input()
			if(isAcross == 'True' or isAcross == 'true'):
				isAcross = True
			else:
				isAcross = False

			print "Enter 0-indexed start position(r c):"
			start = map(int, raw_input().split())
			r,c = start[0],start[1]

			if(isAcross):
				current = [ ourBoard.board[r][c+elem].getChar() for elem in range(len(word)) ]
			else:
				current = [ ourBoard.board[r+elem][c].getChar() for elem in range(len(word)) ]

			valid = True
			for letter in word:
				if (letter not in current) and (letter not in [ t.letter for t in playerRack.rack ]):
					print "Uh oh. Invalid move."
					playerTurn = True 
					valid = False
					break

			if not valid:
				continue
			else:
				for letter in word:
					if letter not in current:

						tiles = [t.letter for t in playerRack.rack]

						for idx, elem in enumerate(tiles):
							if(tiles[idx] == letter):
								del playerRack.rack[idx]
								playerRack.numOfTiles -= 1 
								break

				playerMove(ourBoard, word, (r,c), isAcross)

			
			playerTurn = False
			ourBoard.printBoard()

		while(not playerTurn):
			#Add AI moves here
			playerTurn = True
		
if __name__ == '__main__':
	main()