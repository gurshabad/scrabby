# scrabby
A bot which is better than you at Scrabble


## 1. Setup from source
1. Install dependencies

        
        $ sudo apt-get install python python-pygame termcolor
        
    
2. Clone the repository

        
        $ git clone http://github.com/gurshabad/scrabby.git scrabby
        
        
3. Change directory to the project files and launch the game

        
        $ cd scrabby/projectFiles
        $ python Scrabby.py 2

The command line argument specifies the bot you want to play against.

* 0 -> Monkey (plays random words)
* 1 -> Midas (plays greedily)
* 2 -> Monty (with Monte Carlo lookahead simulations)

Please give the game a few seconds to load. Take this time to think of all the big words your English teacher was trying to teach you while you wasted your time awkwardly sketched on your desk with your little pencil.

## Gameplay
The human player gets the advantage of playing first because we know you're going to lose anyway. For each move, the user interface will ask the following questions in the same order:

#### 1. Shuffle?
Input: Y/N ↩

If you are unsatisfied with your current rack, you can discard some of your current tiles in exchange for new ones. To pass your turn without exchanging any tile, input Y and then press ↩ without entering any characters when prompted.

#### 2. Word
This is the complete primary word you would like to play (including the tiles already on the board). The program will check for validity of the word at this step and the move process will begin again if an unacceptable word is entered. Please find the list of acceptable words here: 

#### 3. Position
This is the position of the tile you'd like the place the first character of your tile on. Do this even if the tile corresponding to the first letter of your word is already on the board. The coordinates for each position can be derived from the displayed board.

Input: <row><column>

eg. 8h corresponds to the center tile
