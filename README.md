# scrabby
A bot which is better than you at Scrabble


## Setup from source
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

Please give the game a few seconds to load. Take this time to think of all the big words your English teacher was trying to teach you while you wasted your time awkwardly sketching on your little desk with your little pencil.

## Gameplay
The human player gets the advantage of playing first because we know you're going to lose anyway. For each move, the user interface will ask the following questions in the same order:

#### 1. Shuffle?
Input: Y/N ↩

If you are unsatisfied with your current rack, you can discard some of your current tiles in exchange for new ones. To pass your turn without exchanging any tile, input Y and then press ↩ without entering any characters when prompted.

#### 2. Word
Input: *sesquipedalophobia* ↩

This is the complete primary word you would like to play (including the tiles already on the board). The program will check for validity of the word at this step and the move process will begin again if an unacceptable word is entered. We're using the standard English Scrabble lexicon.

#### 3. Position
Input: *row**column* ↩

This is the position of the tile you'd like the place the first character of your tile on. Do this even if the tile corresponding to the first letter of your word is already on the board. The coordinates for each position can be derived from the displayed board.

eg. 8h corresponds to the center tile

#### 4. Across?
Input: Y/N ↩
Choose Y to play across the board, or N to play the word down the board.

## Misc.
If you're using a system running on OSX, you can directly launch the game without the source code by downloading [these app files](https://github.com/MayankVachher/scrabby-MacApps).
