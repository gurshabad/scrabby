import sys, pygame, time
from gen_board import *
from tile import *
from rack import *
from trie import *
from inputbox import *

allLetters = "eeeeeeeeeeeeaaaaaaaaaiiiiiiiiioooooooonnnnnnrrrrrrttttttllllssssuuuuddddgggbbccmmppffhhvvwwyykjxqz"

def renderWord(wordPlayed, sanitizedPosition, boardRectangles, playHorizontal, BOARD):
	pos_r = sanitizedPosition[0]
	pos_c = sanitizedPosition[1]

	if(playHorizontal == 'Y'):
		if(pos_r+len(wordPlayed) > 14): return False
		for idx, x in enumerate(wordPlayed):
			renderTile(x, boardRectangles[pos_r+idx][pos_c], BOARD)
	else:
		if(pos_c+len(wordPlayed) > 14): return False
		for idx, x in enumerate(wordPlayed):
			renderTile(x, boardRectangles[pos_r][pos_c+idx], BOARD)
	return True

def renderTile(letter2play, square, BOARD):
	FONTSMALL = pygame.font.SysFont('Andale Mono', 13)
	FONTSMALL2 = pygame.font.SysFont('Andale Mono', 8)
	square = pygame.draw.rect(BOARD, (238, 228, 218), (square.topleft[0], square.topleft[1], square.width, square.height))
	BOARD.blit(FONTSMALL.render(letter2play, 1, (50,50,50)),(square.topleft[0]+10, square.topleft[1]+5))
	BOARD.blit(FONTSMALL2.render(str(Tile(letter2play).getVal()), 1, (50,50,50)),(square.topleft[0]+20, square.topleft[1]+15))

def renderRackTile(letter, score, square, SECONDHALF):
	FONTSMALL = pygame.font.SysFont('Andale Mono', 27)
	FONTSMALL2 = pygame.font.SysFont('Andale Mono', 13)
	square = pygame.draw.rect(SECONDHALF, (238, 228, 218), (square.topleft[0], square.topleft[1], square.width, square.height))
	SECONDHALF.blit(FONTSMALL.render(letter, 1, (50,50,50)),(square.topleft[0]+12, square.topleft[1]+5))
	SECONDHALF.blit(FONTSMALL2.render(str(score), 1, (50,50,50)),(square.bottomright[0] - 10, square.bottomright[1] - 17))

def sanitizePosition(pos):
	if(len(pos) > 4): return False
	if(not pos[0].isalpha()):
		x = ord(pos[-1]) - ord('A')
		pos = pos[:-1]
		pos.strip(" ")
		y = int(''.join(pos)) - 1
		if(x < 15 and x >= 0 and y < 15 and y >= 0):
			return (x,y)
		else: return False
	else:
		x = ord(pos[0]) - ord('A')
		pos = pos[1:]
		pos.strip(" ")
		y = int(''.join(pos)) - 1
		if(x < 15 and x >= 0 and y < 15 and y >= 0):
			return (x,y)
		else: return False

def displayScores(scorePlayer, scoreComputer, inBag, SECONDHALF, SCREEN, PLAYER_MOVE):
	FONT = pygame.font.SysFont('Futura', 27)
	FONT2 = pygame.font.SysFont('Futura', 24)
	humanColor = (175,175,175)
	computerColor = (175,175,175)
	
	if(PLAYER_MOVE): humanColor = (102, 204, 255)
	else: computerColor = humanColor = (102, 204, 255)

	SECONDHALF.blit(FONT.render("HUMAN:", 1, humanColor), (30, 20))
	SECONDHALF.blit(FONT.render(str(scorePlayer), 1, (175,175,175)), (210, 20))
	SECONDHALF.blit(FONT.render("COMPUTER:", 1, computerColor), (30, 60))
	SECONDHALF.blit(FONT.render(str(scoreComputer), 1, (175,175,175)), (210, 60))
	SECONDHALF.blit(FONT2.render("IN BAG", 1, (204, 102, 255)), (340, 20))
	SECONDHALF.blit(FONT2.render(str(inBag), 1, (175, 175, 175)), (370, 60))
	SCREEN.blit(SECONDHALF,(500,0))

def displayRack(rack, SECONDHALF, SCREEN):
	FONT = pygame.font.SysFont('Futura', 27)
	rack.showRack()
	rackSquares = []
	for x in range(7):
		rackSquares.append(pygame.draw.rect(SECONDHALF, (238, 228, 218), (70+(50*x), 155, 40, 40)))
	for idx,element in enumerate(rack.rack):
		if element.letter == " ": pass
		else: renderRackTile(element.letter.upper(), element.value, rackSquares[idx], SECONDHALF)
	SECONDHALF.blit(FONT.render("YOUR RACK", 1, (204, 102, 255)), (170, 200))
	SCREEN.blit(SECONDHALF,(500,0))

def run_game():

	scorePlayer = 0
	scoreComputer = 0

	playerRack = Rack()
	computerRack = Rack()

	bag = [ letter for letter in allLetters ]

	bag = playerRack.replenish(bag)
	bag = computerRack.replenish(bag)

	playerTurn = True

	#------------------------------------------
	#Build Trie

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

	#------------------------------------------
	#Init Board
	ourBoard = TheBoard()

	#------------------------------------------
	#Pygame starts

	pygame.init()
	size = width, height = 1000, 500

	#------------------------------------------
	#Screen Setup

	FONT = pygame.font.SysFont('Andale Mono', 22)
	FONTSMALL = pygame.font.SysFont('Futura', 15)
	FONTSMALL2 = pygame.font.SysFont('Andale Mono', 13)
	WINDOW = pygame.display.set_mode(size)
	CAPTION = pygame.display.set_caption('Scrabby')
	SCREEN = pygame.display.get_surface()
	SCREEN.fill((150, 141, 131))
	FIRSTHALF = pygame.Surface((size[0]/2, size[1]))
	FIRSTHALF.fill((51, 51, 51))
	SECONDHALF = pygame.Surface((size[0]/2, size[1]))
	SECONDHALF.fill((42, 42, 42))
	BOARD = pygame.Surface((462, 462))
	BOARD.fill((10, 10, 10))
	TRANSPARENT = pygame.Surface(size)
	TRANSPARENT.set_alpha(255)
	TRANSPARENT.fill((255,255,255))

	#------------------------------------------
	#board Setup

	boardRectangles = []
	rowMarkers = []
	colMarkers = []
	for x in range(0, 463, 29):
		rowRectangles = []
		for y in range(0, 463, 29):
			if(y == 435):
				if(x == 435): rect = pygame.draw.rect(BOARD, (238, 228, 218), (x,y,29,29))
				else: rect = pygame.draw.rect(BOARD, (238, 228, 218), (x,y,27,29))
			elif(x == 435): rect = pygame.draw.rect(BOARD, (238, 228, 218), (x,y,29,27))
			else: rect = pygame.draw.rect(BOARD, (238, 228, 218), (x,y,27,27))
			
			if(y == 0): colMarkers.append(rect)
			elif(x == 0): rowMarkers.append(rect)
			else: rowRectangles.append(rect)
		
		if(len(rowRectangles) != 0): boardRectangles.append(rowRectangles)

	#Beautify the Board
	for idx, x in enumerate(ourBoard.board):
		for idy, y in enumerate(x):
			myRect = boardRectangles[idx][idy]
			if y.occupied == True: pass #print boardRectangles[idx][idy]
			else:
				if y.special == 4: specialColor = (255, 0, 0) #TW
				elif y.special == 3: specialColor = (255, 153, 255) #DW
				elif y.special == 2: specialColor = (0, 102, 255) #TL
				elif y.special == 1: specialColor = (102, 204, 255) #DL
				else: specialColor = (84, 130, 53)
				myRect = pygame.draw.rect(BOARD, specialColor, (myRect.topleft[0],myRect.topleft[1], myRect.width, myRect.height))
				if y.special == 4: BOARD.blit(FONTSMALL2.render("TW", 1, (50,50,50)),(myRect.topleft[0]+5, myRect.topleft[1]+5))
				elif y.special == 3: BOARD.blit(FONTSMALL2.render("DW", 1, (50,50,50)),(myRect.topleft[0]+5, myRect.topleft[1]+5))
				elif y.special == 2: BOARD.blit(FONTSMALL2.render("TL", 1, (50,50,50)),(myRect.topleft[0]+5, myRect.topleft[1]+5))
				elif y.special == 1: BOARD.blit(FONTSMALL2.render("DL", 1, (50,50,50)),(myRect.topleft[0]+5, myRect.topleft[1]+5))

	#########################################
	#Row-Column Markers to be rendered

	mychar = 'A'

	for idx, x in enumerate(colMarkers):
		if(idx == 0): x = pygame.draw.rect(BOARD, (51, 51, 51), (x.topleft[0], x.topleft[1], x.width+2, x.height+2))
		else:
			x = pygame.draw.rect(BOARD, (51, 51, 51), (x.topleft[0], x.topleft[1], x.width+2, x.height))
			BOARD.blit(FONTSMALL.render(mychar, 1, (200,200,200)),(x.topleft[0]+10, x.topleft[1]+5))
			mychar = chr(ord(mychar) + 1)

	mynum = 1

	for idx, x in enumerate(rowMarkers):
		x = pygame.draw.rect(BOARD, (51, 51, 51), (x.topleft[0], x.topleft[1], x.width, x.height+2))
		BOARD.blit(FONTSMALL.render(str(mynum), 1, (200,200,200)),(x.topleft[0]+5, x.topleft[1]+5))
		mynum += 1


	#-----------------------------------------
	#Refresh Display

	FIRSTHALF.blit(BOARD, (19,19))
	SCREEN.blit(FIRSTHALF,(0,0))
	SCREEN.blit(SECONDHALF,(500,0))
	displayScores(scorePlayer, scoreComputer, len(bag), SECONDHALF, SCREEN, True)
	displayRack(playerRack, SECONDHALF, SCREEN)
	pygame.display.flip()

	#-----------------------------------------
	#Main Loop

	ourBoard.printBoard()
	while True:
		pos = pygame.mouse.get_pos()
		mouse = pygame.draw.circle(TRANSPARENT, (0,0,0), pos, 0)
		
		#------------------------------------
		#Detect Events

		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			else:
				playHorizontal = ask(SCREEN, SECONDHALF, "Horizontal?(YES/NO)")
				playHorizontal = (playHorizontal).upper()
				if(playHorizontal != "YES" and playHorizontal != "NO" and playHorizontal != "Y" and playHorizontal != "N"):
					print "\nHorizontal? WEIRD INPUT"
					SECONDHALF.blit(FONT.render("WEIRD INPUT! TRY AGAIN!", 1, (255,0,0)),
                	((SECONDHALF.get_width() / 2) - 200, (SECONDHALF.get_height() / 2) + 170))
					SCREEN.blit(SECONDHALF, (500,0))
					pygame.display.flip()
					time.sleep(3)
					break
				else:
					playHorizontal = playHorizontal[0]
					if playHorizontal == 'Y': print "\nHorizontal? Y"
					else: print "\nHorizontal? N"
					
					wordPlayed = ask(SCREEN, SECONDHALF, "WORD?")
					if(wordListTrie.query(wordPlayed.lower())): #Check if legit word
						print "Word? " + wordPlayed
						positionPlayed = ask(SCREEN, SECONDHALF, "POSITION? (ROW COL)")
						sanitizedPos = sanitizePosition(positionPlayed)
						if(sanitizedPos != False): #Check if legit position
							print "Position? " + positionPlayed
							print "After Sanitization: "+str(sanitizedPos)
							if not (renderWord(wordPlayed, sanitizedPos, boardRectangles, playHorizontal, BOARD)):
								print "Error. Invalid Move."
							else:
								FIRSTHALF.blit(BOARD, (19,19))
								SCREEN.blit(FIRSTHALF,(0,0))
								pygame.display.flip()
								print "Success!"
						else:
							print "Position? " + positionPlayed + " - Invalid Position!"
							SECONDHALF.blit(FONT.render("Invalid Position! TRY AGAIN!", 1, (255,0,0)),
                			((SECONDHALF.get_width() / 2) - 200, (SECONDHALF.get_height() / 2) + 170))
							SCREEN.blit(SECONDHALF, (500,0))
							pygame.display.flip()
							time.sleep(3)
							break
					else:
						print "Word? " + wordPlayed + " - This word does not exist!"
						SECONDHALF.blit(FONT.render("Word is Non-existent! TRY AGAIN!", 1, (255,0,0)),
                		((SECONDHALF.get_width() / 2) - 200, (SECONDHALF.get_height() / 2) + 170))
						SCREEN.blit(SECONDHALF, (500,0))
						pygame.display.flip()
						time.sleep(3)
						break
				pygame.display.flip()

def main():
	run_game()

if __name__ == '__main__':
	main()