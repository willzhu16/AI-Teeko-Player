import random

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def run_challenge_test(self):
        """ Set to True if you would like to run gradescope against the challenge AI!
        Leave as False if you would like to run the gradescope tests faster for debugging.
        You can still get full credit with this set to False
        """ 
        return False

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
       """
        #Check if you can win
        for succ, move in self.succ(state):
            if self.game_value(succ) == 1:
                return move  #

        drop_phase = sum(row.count('b') + row.count('r') for row in state) < 8
        _, best_move = self.minimax(state, depth=3, alpha=float('-inf'), beta=float('inf'), is_max_turn=True)
        return best_move


    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
        
    # Function as described in class 
    def minimax(self, state, depth, alpha, beta, is_max_turn):
        
        #Check if game is already over.
        if self.game_value(state) != 0:
            return self.game_value(state), None
        if depth == 0:
            return self.heuristic_game_value(state), None

        successors = self.succ(state)
        
        #Sort for efficiency
        successors = sorted(successors, key=lambda x: self.heuristic_game_value(x[0]), reverse=is_max_turn)

        best_move = None
        if is_max_turn:
            value = float('-inf')
            for succ_state, move in successors:
                val, _ = self.minimax(succ_state, depth - 1, alpha, beta, False)
                if val > value:
                    value = val
                    best_move = move
                alpha = max(alpha, value)
                
                #Pruning
                if alpha >= beta:
                    break 
            return value, best_move
        else:
            value = float('inf')
            for succ_state, move in successors:
                val, _ = self.minimax(succ_state, depth - 1, alpha, beta, True)
                if val < value:
                    value = val
                    best_move = move
                beta = min(beta, value)
                
                #Pruning
                if alpha >= beta:
                    break  
            return value, best_move


    #Generates the options the player can take.
    def succ(self, state):
        successors = []
        
        # Used to determine phase.
        total_pieces = sum(row.count('b') + row.count('r') for row in state)

        if total_pieces < 8:
            # Still in drop phase - add a piece in any open space.
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ':
                        new_state = [row[:] for row in state]
                        new_state[i][j] = self.my_piece
                        move = [(i, j)]
                        successors.append((new_state, move))
        else:
            # Move phase - move a piece to an empty spot. 
            for i in range(5):
                for j in range(5):
                    
                    #Get all pieces and try moving them 
                    if state[i][j] == self.my_piece:
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                
                                #Same position
                                if dx == 0 and dy == 0:
                                    continue
                                new_i, new_j = i + dx, j + dy
                                
                                #Save all valid configurations
                                if 0 <= new_i < 5 and 0 <= new_j < 5 and state[new_i][new_j] == ' ':
                                    new_state = [row[:] for row in state]
                                    new_state[i][j] = ' '
                                    new_state[new_i][new_j] = self.my_piece
                                    move = [(new_i, new_j), (i, j)]
                                    successors.append((new_state, move))
        return successors


    #Heuristic - lines in a row and partial blocks give points.
    def heuristic_game_value(self, state):
        # Check for win
        winner = self.game_value(state)
        if winner != 0:
            return float(winner)

        #Helps count lines
        def count_line_pieces(line, piece):
            count = 0
            max_count = 0
            for cell in line:
                if cell == piece:
                    count += 1
                    max_count = max(max_count, count)
                else:
                    count = 0
            return max_count

        #Helps count boxes 
        def box_score(state, piece):
            score = 0
            for i in range(4):
                for j in range(4):
                    cells = [
                        state[i][j],
                        state[i][j+1],
                        state[i+1][j],
                        state[i+1][j+1]
                    ]
                    count = sum(1 for cell in cells if cell == piece)
                    if count == 3:
                        score += 0.75
                    elif count == 2:
                        score += 0.3
                    elif count == 1:
                        score += 0.1
            return score

        #Checks for lines 
        def max_chain(state, piece):
            max_len = 0
            for i in range(5):
                row = state[i]
                col = [state[r][i] for r in range(5)]
                max_len = max(max_len, count_line_pieces(row, piece))
                max_len = max(max_len, count_line_pieces(col, piece))
            for i in range(-1, 2):
                diag1 = [state[x][x+i] for x in range(5) if 0 <= x+i < 5]
                diag2 = [state[x][4-x+i] for x in range(5) if 0 <= 4-x+i < 5]
                max_len = max(max_len, count_line_pieces(diag1, piece))
                max_len = max(max_len, count_line_pieces(diag2, piece))
            return max_len

        # Gives center a bonus
        def center_bonus(state, piece):
            bonus = 0
            for i in range(5):
                for j in range(5):
                    if state[i][j] == piece:
                        bonus += 2 - abs(2 - i) - abs(2 - j)
            return bonus

        #Checks for immediate win conditions.
        def opponent_can_win_next(state):
            original_piece = self.my_piece
            original_opp = self.opp
            self.my_piece = self.opp
            self.opp = original_piece

            for succ_state, _ in self.succ(state):
                if self.game_value(succ_state) == 1:
                    self.my_piece = original_piece
                    self.opp = original_opp
                    return True

            self.my_piece = original_piece
            self.opp = original_opp
            return False

        if opponent_can_win_next(state):
            return -0.99

        # Weights
        w_line = 1.0
        w_box = 1.5
        if sum(row.count('b') + row.count('r') for row in state) < 8:
            w_center = 1.0
        else:
            w_center = 0.1
        w_threat = 3.0

        my_score = (
            w_line * max_chain(state, self.my_piece)
        + w_box * box_score(state, self.my_piece)
        + w_center * center_bonus(state, self.my_piece)
        )

        opp_score = (
            w_line * max_chain(state, self.opp)
        + w_box * box_score(state, self.opp)
        + w_center * center_bonus(state, self.opp)
        )

        threat_penalty = w_threat * opponent_can_win_next(state)

        return (my_score - (opp_score + threat_penalty)) / 40.0



    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # \ diagonal wins 
        for i in range(2):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                    return 1 if state[i][j] == self.my_piece else -1

        # / diagonal wins    
        for i in range(2):
            for j in range(3, 5):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
                    return 1 if state[i][j] == self.my_piece else -1

        # check box wins
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i][j+1] == state[i+1][j] == state[i+1][j+1]:
                    return 1 if state[i][j] == self.my_piece else -1

        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is your AI opponent')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
