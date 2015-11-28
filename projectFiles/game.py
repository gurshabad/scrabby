#List of conventions

# All lowercase letters in backend
# 0-indexing

#List ends

from gen_board import *
from tile import *
from rack import *
from trie import *
from helpers import *
from copy import deepcopy
import random
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



def setCrossCheckBits(board, wordList):

	#Set acrossCrossCheck Bits

	for i in xrange(15):
		for j in xrange(15):

			partialFrontWord = ''
			partialBackWord = ''

			if(i < 14):
				if(board.board[i+1][j].occupied):

					k=1
					while(board.board[i+k][j].occupied):
						partialFrontWord =  partialFrontWord + board.board[i+k][j].getChar()
						k += 1
						if(i+k>14):
							break
			if(i > 0):
				if(board.board[i-1][j].occupied):

					k=1
					while(board.board[i-k][j].occupied):
						partialBackWord = board.board[i-k][j].getChar() + partialBackWord
						k += 1
						if(i-k<0):
							break

			for letNo in xrange(26):
				letter = chr(letNo + ord('a'))
				word = partialBackWord + letter + partialFrontWord

				if(len(word) > 1):

					if(wordList.query(word)):
						board.board[i][j].acrossCrossCheck[letNo] = True
					else:
						board.board[i][j].acrossCrossCheck[letNo] = False

	#Set downCrossCheck Bits

	for i in xrange(15):
		for j in xrange(15):

			partialFrontWord = ''
			partialBackWord = ''

			if(j < 14):
				if(board.board[i][j+1].occupied):

					k=1
					while(board.board[i][j+k].occupied):
						partialFrontWord =  partialFrontWord + board.board[i][j+k].getChar()
						k += 1
						if(j+k>14):
							break
			if(j > 0):
				if(board.board[i][j-1].occupied):

					k=1
					while(board.board[i][j-k].occupied):
						partialBackWord = board.board[i][j-k].getChar() + partialBackWord
						k += 1
						if(j-k<0):
							break

			for letNo in xrange(26):
				letter = chr(letNo + ord('a'))
				word = partialBackWord + letter + partialFrontWord
				if(len(word) > 1):
					if(wordList.query(word)):
						board.board[i][j].downCrossCheck[letNo] = True
					else:
						board.board[i][j].downCrossCheck[letNo] = False


def validityCheck(isAcross, board, pos, word, playerRack):

	print word, pos, isAcross

	r = pos[1]
	c = pos[0]

	#Check 1: Check if word stays within bounds of the board

	if(isAcross):
		if(c+len(word) > 15): 
			print "Uh oh #1 Invalid move."
			return False

	else:
		if(r+len(word) > 15): 
			print "Uh oh #1 Invalid move."
			return False

	#word = word.lower()
	#print word

	#Get a snapshot of the board at the desired positions

	if(isAcross):
		current = [ board.board[r][c+elem] for elem in range(len(word)) ]
	else:
		current = [ board.board[r+elem][c] for elem in range(len(word)) ]

	print [ c.getChar() for c in current ]

	rackCopy = [ t.letter for t in playerRack.rack ]
	deleteThis = []

	anchorFlag = False

	#Check 2: Check if we even have the letters not on the board on our rack.
	#Check 3: Check if letters on the board line up with letters in the word.
	#Check 4: Check if we are using atleast one anchor square.
	#Check 5: Check if we're not creating new nonsense words 

	for idx, letter in enumerate(word):

		if(anchorFlag == False):
			anchorFlag = current[idx].isAnchor
		if( current[idx].getChar() == '_'):  #If blank position
			if (letter not in rackCopy): #Check if we even have the letter in our rack.
				print "Uh oh #2 Invalid move."
				return False
			else:
				rackCopy.remove(letter) #If we do, remove it from future matches. Its booked.
				deleteThis.append(letter)

			if(isAcross):
				if not current[idx].acrossCrossCheck[ord(letter)-ord('a')]:
					print "Uh oh #5 Invalid move. Extra nonsense words."
					return False
			else:
				if not current[idx].downCrossCheck[ord(letter)-ord('a')]:
					print "Uh oh #5 Invalid move. Extra nonsense words."
					return False
				

		elif(current[idx].getChar() != letter): #If not blank position but letter does not match.
			print "Uh oh #3 Invalid move."
			return False

		#If not blank and letter matches, just continue cuz everything is chill.

	if not anchorFlag:
		print "Uh oh #4 Invalid move."
		return False

	#Return list of letters to be removed from the rack.
	return ''.join(deleteThis)



#The following function just sets the tiles in the backend board and sets adjacent squares to Anchor 
def playerMove(board, word, pos, isAcross):

	#word = word.lower()

	if(isAcross):

		if not pos[0] == 0:
			if board.board[pos[1]][pos[0]-1].occupied == False:
				board.board[pos[1]][pos[0]-1].isAnchor = True
		if not pos[0] + len(word)-1 == 14:
			if board.board[pos[1]][pos[0]+len(word)].occupied == False:
				board.board[pos[1]][pos[0]+len(word)].isAnchor = True

		for loc, letter in enumerate(word):
			if not pos[1] == 14:
				if board.board[pos[1]+1][pos[0]+loc].occupied == False :				
					board.board[pos[1]+1][pos[0]+loc].isAnchor = True
			if not pos[1] == 0:
				if board.board[pos[1]-1][pos[0]+loc].occupied == False:
					board.board[pos[1]-1][pos[0]+loc].isAnchor = True

			board.board[pos[1]][pos[0]+loc].isAnchor = False

			board.board[pos[1]][pos[0]+loc].setTile(Tile(letter))

			print board.board[pos[1]][pos[0]+loc].getChar(), pos[1], pos[0]+loc, board.board[pos[1]][pos[0]+loc].isAnchor


	else:

		if not pos[1] == 0:
			if board.board[pos[1]-1][pos[0]].occupied == False:
				board.board[pos[1]-1][pos[0]].isAnchor = True
		if not pos[1] + len(word)-1 == 14:
			if board.board[pos[1]+len(word)][pos[0]].occupied == False:
				board.board[pos[1]+len(word)][pos[0]].isAnchor = True

		for loc, letter in enumerate(word):
			if not pos[0] == 14:
				if board.board[pos[1]+loc][pos[0] + 1].occupied == False:
					board.board[pos[1]+loc][pos[0] + 1].isAnchor = True
			if not pos[0] == 0:
				if board.board[pos[1]+loc][pos[0]-1].occupied == False:
					board.board[pos[1]+loc][pos[0]-1].isAnchor = True

			board.board[pos[1]+loc][pos[0]].isAnchor = False

			board.board[pos[1]+loc][pos[0]].setTile(Tile(letter))
			print board.board[pos[1]+loc][pos[0]].getChar(), pos[1]+loc, pos[0], board.board[pos[1]+loc][pos[0]].isAnchor


#This function calculates the score of a move after it has been played
def scoreThisMove(board, word, pos, isAcross):
	r = pos[1]
	c = pos[0]
	#Get relevant space

	if(isAcross):
		current = [ board.board[r][c+elem] for elem in range(len(word)) ]

	else:
		current = [ board.board[r+elem][c] for elem in range(len(word)) ]

	for i in range(len(word)):
		if current[i].getChar() == '_':
			current[i].setTileVal(Tile(word[i]))

	""" Tile special codes for reference
	0 - Nothing Special
	1 - Double Letter(DL)
	2 - Triple Letter(TL)
	3 - Double Word(DW)
	4 - Triple Word(TW)
	"""
	finalScore = 0

	if(isAcross):
		#check for bingo
		tileCount = 0
		for tile in current:
			if not tile.occupied:
				tileCount += 1
		if tileCount == 7:
			finalScore += 50

		#calculate score for the main word formed
		mainWordScore = 0
		numDW = 0 #number of double word premium tiles
		numTW = 0 #number of triple word premium tiles
		for t in current:
			if t.occupied:
				mainWordScore += t.tile.getVal()
			else:
				if t.special == 0:
					mainWordScore += t.tile.getVal()
				elif t.special == 1:
					mainWordScore += 2 * t.tile.getVal()
				elif t.special == 2:
					mainWordScore += 3 * t.tile.getVal()
				elif t.special == 3:
					mainWordScore += t.tile.getVal()
					numDW += 1
				elif t.special == 4:
					mainWordScore += t.tile.getVal()
					numTW += 1

		if numDW > 0:
			mainWordScore *= numDW * 2
		if numTW > 0:
			mainWordScore *= numTW * 3

		finalScore += mainWordScore

		#calculate score for words that are made up and down
		for colno in range(c, c+len(word)):
			if not board.board[r][colno].occupied:
				upFlag = False
				downFlag = False
				if r > 0:
					if (board.board[r-1][colno].occupied):
						upFlag = True
				if r < 14:
					if (board.board[r+1][colno].occupied):
						downFlag = True

				#check next column if no word formed here
				if not upFlag and not downFlag:
					continue

				upStart = r
				downStart = r

				if upFlag and upStart > 0:
					while board.board[upStart-1][colno].occupied:
						upStart -= 1
						if upStart == 0:
							break

				if downFlag and downStart < 14:
					while board.board[downStart+1][colno].occupied:
						downStart += 1
						if downStart == 15:
							break

				#start scoring word
				wordScore = 0
				if board.board[r][colno].special == 1:
					wordScore += 2 * board.board[r][colno].tile.getVal()
				if board.board[r][colno].special == 2:
					wordScore += 3 * board.board[r][colno].tile.getVal()

				currentWordSquares = [ board.board[elem][colno] for elem in range(upStart, downStart+1)]
				for currentSquare in currentWordSquares:
					if currentSquare.occupied:
						wordScore += currentSquare.tile.getVal()

				if board.board[r][colno].special == 3:
					wordScore = 2 * wordScore

				if board.board[r][colno].special == 4:s
					wordScore = 3 * wordScore

				finalScore += wordScore

	else:
		#check for bingo
		tileCount = 0
		for tile in current:
			if not tile.occupied:
				tileCount += 1
		if tileCount == 7:
			finalScore += 50

		#calculate score for the main word formed
		mainWordScore = 0
		numDW = 0 #number of double word premium tiles
		numTW = 0 #number of triple word premium tiles
		for t in current:
			if t.occupied:
				mainWordScore += t.tile.getVal()
			else:
				if t.special == 0:
					mainWordScore += t.tile.getVal()
				elif t.special == 1:
					mainWordScore += 2 * t.tile.getVal()
				elif t.special == 2:
					mainWordScore += 3 * t.tile.getVal()
				elif t.special == 3:
					mainWordScore += t.tile.getVal()
					numDW += 1
				elif t.special == 4:
					mainWordScore += t.tile.getVal()
					numTW += 1

		if numDW > 0:
			mainWordScore *= numDW * 2
		if numTW > 0:
			mainWordScore *= numTW * 3

		finalScore += mainWordScore

		#calculate score for words that are made left and right
		for rowno in range(r, r+len(word)):
			if not board.board[rowno][c].occupied:
				leftFlag = False
				rightFlag = False
				if c > 0:
					if (board.board[rowno][c-1].occupied):
						leftFlag = True
				if c < 14:
					if (board.board[rowno][c+1].occupied):
						rightFlag = True

				#check next row if no word formed here
				if not leftFlag and not rightFlag:
					continue

				leftStart = c
				rightStart = c

				if leftFlag and leftStart > 0:
					while board.board[rowno][leftStart-1].occupied:
						leftStart -= 1
						if leftStart == 0:
							break

				if rightFlag and rightStart < 14:
					while board.board[rowno][rightStart+1].occupied:
						rightStart += 1
						if rightStart == 15:
							break

				#start scoring word
				wordScore = 0
				if board.board[rowno][c].special == 1:
					wordScore += 2 * board.board[rowno][c].tile.getVal()
				if board.board[rowno][c].special == 2:
					wordScore += 3 * board.board[rowno][c].tile.getVal()

				currentWordSquares = [ board.board[rowno][elem] for elem in range(leftStart, rightStart+1)]
				for currentSquare in currentWordSquares:
					if currentSquare.occupied:
						wordScore += currentSquare.tile.getVal()

				if board.board[rowno][c].special == 3:
					wordScore = 2 * wordScore

				if board.board[rowno][c].special == 4:
					wordScore = 3 * wordScore

				finalScore += wordScore

	#print "Final score calculated: ", finalScore
	return finalScore


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


def leftPart(board, rowIdx, rack, partialWord, currentNode, anchorSquare, limit, legalWords):

	#Case 1: Left of anchor square occupied

	#print "wtf\n"

	if anchorSquare > 0:
		if(board[rowIdx][anchorSquare-1].getChar() != '_'):

			#print "THIS HAPPENED\n"
			leftSquare = anchorSquare-1
			leftBit = board[rowIdx][leftSquare].getChar()

			#Construct the existing leftPart
			while(leftSquare > 0):

				if(board[rowIdx][leftSquare-1].getChar() == '_'):
					break

				leftSquare = leftSquare - 1

				leftBit = board[rowIdx][leftSquare].getChar() + leftBit

			#Walk down the trie to node with leftBit path

			for element in leftBit:
				if element in currentNode.children:
					currentNode = currentNode.children[element]
				else:
					return

			#For each tile playable on anchorSquare

			for child in currentNode.children:
				if child in rack:
					#print "HEREIAM", board[rowIdx][anchorSquare].acrossCrossCheck[ord(child)-ord('a')]
					if board[rowIdx][anchorSquare].acrossCrossCheck[ord(child)-ord('a')] == True:
						rack.remove(child)
						extendRightBeta(board, rowIdx, rack, leftBit + child, currentNode.children[child], anchorSquare, legalWords, anchorSquare)
						rack.append(child)

		#Case 2: Left of anchor square vacant
		else:

			#print "NO, THIS HAPPENED\n"

			#For each tile playable on anchorSquare

			#print partialWord, limit

			pStart = anchorSquare - len(partialWord)

			for i, letter in enumerate(partialWord):
				if board[rowIdx][pStart+i].acrossCrossCheck[ord(letter)-ord('a')] == False:
					return 

			#print partialWord, limit, "survived!"

			for child in currentNode.children:
				if child in rack: 
					if board[rowIdx][anchorSquare].acrossCrossCheck[ord(child)-ord('a')] == True:
						rack.remove(child)
						extendRightBeta(board, rowIdx, rack, partialWord + child, currentNode.children[child], anchorSquare, legalWords, anchorSquare)
						rack.append(child)

			if limit > 0:
				for child in currentNode.children:
					if child in rack:
						rack.remove(child)
						leftPart( board, rowIdx, rack, partialWord + child, currentNode.children[child], anchorSquare, limit-1, legalWords)
						rack.append(child)
	else:
		for child in currentNode.children:
			if child in rack:
				if board[rowIdx][anchorSquare].acrossCrossCheck[ord(child)-ord('a')] == True:
					rack.remove(child)
					extendRightBeta(board, rowIdx, rack, partialWord + child, currentNode.children[child], anchorSquare, legalWords, anchorSquare)
					rack.append(child)

	#return legalWords

#extendRightBeta notes-
#The below function considers the situation at each step where:
#partialWord[:-1](partialWord without last letter) is already on the board
#We are looking to add currentNode to the end of partialWord[:-1]
#The validity of placing currentNode has already been checked (partialWord is some valid prefix)

def extendRightBeta(board, rowIdx, rack, partialWord, currentNode, square, legalWords, anchorSquare):

	#Case 1: At the board's edge. Play currentNode and check validity of partialWord.
	if(square == 14):
		if '{' in currentNode.children:
			colIdx = square - len(partialWord) + 1
			legalWords.append((partialWord, (colIdx, rowIdx), True, (anchorSquare, rowIdx)))

	#Case 2: Still looking to place more tiles on the board after this move if we can
	else:
		#Case 2.1: If square next to where we want to place letter on currentNode on is empty.
		if(board[rowIdx][square+1].getChar() == '_'): 

			#Play and check if partial word is legal.

			if '{' in currentNode.children:
				colIdx = square - len(partialWord) + 1
				legalWords.append((partialWord, (colIdx, rowIdx), True, (anchorSquare, rowIdx) ))

			#Find a candidate tile to play at the next square and call extendRight on it
			for child in currentNode.children:
				if child in rack:
					if board[rowIdx][square+1].acrossCrossCheck[ord(child)-ord('a')] == True:  #and it can be legally placed on the next square.
						rack.remove(child)
						extendRightBeta(board, rowIdx, rack,partialWord + child, currentNode.children[child], square + 1, legalWords, anchorSquare)
						rack.append(child)

		#Case 2.2: If square next to where we want to place letter from currentNode on is full. Hey, no worries!
		#Just check if playing the occupying letter after currentNode will give us some valid prefix 
		else:
			if board[rowIdx][square+1].getChar() in currentNode.children:
				extendRightBeta(board, rowIdx, rack, partialWord + board[rowIdx][square+1].getChar(), currentNode.children[board[rowIdx][square+1].getChar()], square + 1, legalWords, anchorSquare)


def upperPart(board, colIdx, rack, partialWord, currentNode, anchorSquare, limit, legalWords):

	#Case 1: Above of anchor square occupied
	if anchorSquare > 0:
		if(board[anchorSquare-1][colIdx].getChar() != '_'):

			#print "THIS HAPPENED\n"
			upSquare = anchorSquare-1
			upBit = board[upSquare][colIdx].getChar()

			#Construct the existing upPart
			while(upSquare > 0):

				if(board[upSquare-1][colIdx].getChar() == '_'):
					break

				upSquare = upSquare - 1

				upBit = board[upSquare][colIdx].getChar() + upBit

			#Walk down the trie to node with upBit path. If it exists. 
			for element in upBit:
				if element in currentNode.children:
					currentNode = currentNode.children[element]
				else:
					return

			#For each tile playable on anchorSquare
			for child in currentNode.children:
				if child in rack: 
					if board[anchorSquare][colIdx].downCrossCheck[ord(child)-ord('a')] == True:
						rack.remove(child)
						extendDownBeta(board, colIdx, rack, upBit + child, currentNode.children[child], anchorSquare, legalWords, anchorSquare)
						rack.append(child)

		#Case 2: Left of anchor square vacant
		else:

			##print "NO, THIS HAPPENED\n"


			#print partialWord, limit

			pStart = anchorSquare - len(partialWord)

			for i, letter in enumerate(partialWord):
				if board[pStart+i][colIdx].downCrossCheck[ord(letter)-ord('a')] == False:
					return 

			#print partialWord, limit, "survived!"


			#For each tile playable on anchorSquare
			for child in currentNode.children:
				if child in rack:
					if board[anchorSquare][colIdx].downCrossCheck[ord(child)-ord('a')] == True:
						rack.remove(child)
						extendDownBeta(board, colIdx, rack, partialWord + child, currentNode.children[child], anchorSquare, legalWords, anchorSquare)
						rack.append(child)

			if limit > 0:
				for child in currentNode.children:
					if child in rack:
						rack.remove(child)
						upperPart( board, colIdx, rack, partialWord + child, currentNode.children[child], anchorSquare, limit-1, legalWords)
						rack.append(child)

	else:

		for child in currentNode.children:
			if child in rack:
				if board[anchorSquare][colIdx].downCrossCheck[ord(child)-ord('a')] == True:
					rack.remove(child)
					extendDownBeta(board, colIdx, rack, partialWord + child, currentNode.children[child], anchorSquare, legalWords, anchorSquare)
					rack.append(child)

	#return legalWords

#extendRightBeta notes-
#The below function considers the situation at each step where:
#partialWord[:-1](partialWord without last letter) is already on the board
#We are looking to add currentNode to the end of partialWord[:-1]
#The validity of placing currentNode has already been checked (partialWord is some valid prefix)

def extendDownBeta(board, colIdx, rack, partialWord, currentNode, square, legalWords, anchorSquare):

	#Case 1: At the board's edge. Play currentNode and check validity of partialWord.
	if(square == 14):
		if '{' in currentNode.children:
			rowIdx = square - len(partialWord) + 1
			legalWords.append((partialWord, (colIdx, rowIdx), False, (colIdx, anchorSquare) ))

	#Case 2: Still looking to place more tiles on the board after this move if we can
	else:
		#Case 2.1: If square next to where we want to place letter on currentNode on is empty.
		if(board[square+1][colIdx].getChar() == '_'): 

			#Play and check if partial word is legal.   
			if '{' in currentNode.children:
				rowIdx = square - len(partialWord) + 1
				legalWords.append((partialWord, (colIdx, rowIdx), False, (colIdx, anchorSquare) ))

			#Find a candidate tile to play at the next square and call extendRight on it
			for child in currentNode.children:
				if child in rack:
					if board[square+1][colIdx].downCrossCheck[ord(child)-ord('a')] == True:  #and it can be legally placed on the next square.
						rack.remove(child)
						extendDownBeta(board, colIdx, rack,partialWord + child, currentNode.children[child], square + 1, legalWords, anchorSquare)
						rack.append(child)

		#Case 2.2: If square next to where we want to place letter from currentNode on is full. Hey, no worries!
		#Just check if playing the occupying letter after currentNode will give us some valid prefix 
		else:
			if board[square+1][colIdx].getChar() in currentNode.children:
				extendDownBeta(board, colIdx, rack, partialWord + board[square+1][colIdx].getChar(), currentNode.children[board[square+1][colIdx].getChar()], square + 1, legalWords, anchorSquare)



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



#Below is a honorable sandbox to play with extendLeft and extendRightBeta
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



		ourBoard.board[7][7].isAnchor = True


		while(playerTurn):

			#User input.

			setCrossCheckBits(ourBoard, wordListTrie)
			bag = playerRack.replenish(bag)

			playerRack.showRack()


			print "Enter number of tiles you wanna play:"
			wordLength = input()
			print "Enter word:"
			word = raw_input()
			if not wordListTrie.query(word):
				print "\nSorry, not a word. Try again.\n"
				continue

			print "Enter 'True' if across else 'False':"
			isAcross = raw_input()
			if(isAcross == 'True' or isAcross == 'true'):
				isAcross = True
			else:
				isAcross = False

			print "Enter 0-indexed start position(r c):"
			start = map(int, raw_input().split())
			r,c = start[0],start[1]

			#Validity checking.
			current = validityCheck(isAcross, ourBoard, (c,r), word, playerRack)

			if not current:
				print "Try again."
				continue
			else:
				playerRack = removeTiles(playerRack, current)
				playerMove(ourBoard, word, (c,r), isAcross)
				playerTurn = False
				ourBoard.printBoard()

		while(not playerTurn):
			#Add AI moves here

			setCrossCheckBits(ourBoard, wordListTrie)

			bag = computerRack.replenish(bag);

			computerRack.showRack()


			# playerTurn = True
			# continue

			rack = [ i.letter for i in computerRack.rack]

			anchorSquare = 6
			legalWords = []
			leftPart(ourBoard.board, 7, rack, '', wordListTrie.root, anchorSquare, 4, legalWords)

			print legalWords

			#List of 4-tuples: (word, pos, isAcross)			
			# # legalWords = []

			# # #Generate all across moves
			# # for rowIdx, row in enumerate(ourBoard.board):
			# # 	for idx, sq in enumerate(row):
			# # 		prevAnchor = -1
			# # 		if sq.isAnchor:

			# # 			limit = min(idx, idx-prevAnchor-1)
			# # 			anchorSquare = idx
			# # 			prevAnchor = anchorSquare

			# # 			leftPart(ourBoard.board, rowIdx, rack, '', wordListTrie.root, anchorSquare, limit, legalWords)

			# #Generate all down moves
			# for colIdx in xrange(len(ourBoard.board)):
			# 	for rowIdx in xrange(len(ourBoard.board)):
			# 		prevAnchor = -1
			# 		sq = ourBoard.board[rowIdx][colIdx]
			# 		if sq.isAnchor:

			# 			limit = min(rowIdx, rowIdx-prevAnchor-1)
			# 			anchorSquare = rowIdx
			# 			prevAnchor = anchorSquare

			# 			upperPart(ourBoard.board, colIdx, rack, '', wordListTrie.root, anchorSquare, limit, legalWords)
	

			random.shuffle(legalWords)

			if(len(legalWords)):
				current = validityCheck(legalWords[0][2], ourBoard, legalWords[0][1], legalWords[0][0], computerRack)

				if not current:
					print "Try again."
					continue
				else:
					computerRack = removeTiles(computerRack, current)
					playerMove(ourBoard,legalWords[0][0], legalWords[0][1], legalWords[0][2])
					playerTurn = True
					ourBoard.printBoard()

			else:
				playerTurn = True
				continue
			
if __name__ == '__main__':
	main()
