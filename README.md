# AI-Teeko-Player

Teeko is a simple 2 player game featuring a 5 × 5 board. Players take turns placing 4 markers each during the drop phase. If neither player has won, they take turns moving one of their pieces to an adjacent empty square - diagonals included. 

Wrap around win conditions are not considered. 

#Win Conditions:
- 4 pieces in a line [horizontal, vertical, or diagonal]
- 4 pieces in a 2x2 square. 

# Implementation

We use a minimax tree with pruning to calculate the best move for the AI opponent. With a depth of three, the tree allows for efficient move selection while playing intelligently.   

# How to play
- Run the code using 
```bash
python game.py
```

- The AI will go first - their pieces are 'b' for black.
- You are red ('r')
- Try to win!!!


