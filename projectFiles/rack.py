from tile import *

class Rack:
	rack = []
	def __init__(self):
		for i in range(7):
			self.rack.append(Tile())

	def showRack(self):
		print "Current Rack"
		print "-------------"
		print "Letter:\t",
		for x in self.rack:
			if x.letter == " ": print "blank tile",
			else: print x.letter,
		print "\nScore:\t",
		for x in self.rack:
			if x.value == -1: print "_",
			else: print x.value,



def main():
	myRack = Rack()
	myRack.rack[2] = Tile('A')
	myRack.showRack()

if __name__ == '__main__':
	main()