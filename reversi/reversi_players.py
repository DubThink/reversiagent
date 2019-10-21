# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy


class HumanPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        # Let the player type in their move.
        # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
        valid_digits = []
        for i in range(1, board.get_size()+1):
            valid_digits.append(str(i))
        no_valid_move = True
        while no_valid_move:
            move = input(self.symbol + ', enter your move:').lower()
            if len(move) == 2 and move[0] in valid_digits and move[1] in valid_digits:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if board.is_valid_move(self.symbol, ( x, y) ):
                    no_valid_move = False
                    return [x, y]
                else:
                    print('Not a valid move.')
            else:
                print('Bad input. Type valid x digit, then the y digit.')


class RandomComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        return random.choice(board.calc_valid_moves(self.symbol))


"""
Simple greedy agent
@author B Welsh
"""
class ReallyGreatPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        max_move=None
        max_move_val=0
        for move in board.calc_valid_moves(self.symbol):
            m_val=len(board.is_valid_move(self.symbol,move))
            if m_val>max_move_val:
                max_move=move
                max_move_val=m_val
        return max_move


"""
Simple greedy agent
@author Molly Noel
"""
class GreedyComputerPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        score=board.calc_scores()[self.symbol]
        max_pieces_captured=0
        for move in board.calc_valid_moves(self.symbol):
            board_copy=copy.deepcopy(board)
            board_copy.make_move(self.symbol,move)
            pieces_captured=board_copy.calc_scores()[self.symbol]-score
            if pieces_captured>max_pieces_captured:
                max_pieces_captured=pieces_captured
                best_move=move
        return best_move


"""
Modified greedy agent that prioritizes edges
@author B Welsh
"""
class FantasticPlayerWow:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        # print('fantastic move wow')
        max_move = None
        max_move_val = 0
        for move in board.calc_valid_moves(self.symbol):
            m_val = len(board.is_valid_move(self.symbol, move))
            if move[0] is 0 or move[0] is board.get_size()-1:
                m_val*=1.2
            if move[1] is 0 or move[1] is board.get_size()-1:
                m_val*=1.2
            if m_val > max_move_val:
                max_move = move
                max_move_val = m_val
        return max_move

"""
Returns opposite symbol
@author B Welsh
"""
def opposite_symbol(sym):
    if sym is "X":
        return "O"
    return "X"


"""
minimax agent
@author B Welsh
"""
class MinimaxPlayerHowGreat:

    def __init__(self, symbol):
        self.symbol = symbol


    def get_move(self, board):
        # print('minimax move')
        max_move = None
        max_move_val = -10000
        for move in board.calc_valid_moves(self.symbol):
            m_val = minimax(board,move,self.symbol)
            if m_val > max_move_val:
                max_move = move
                max_move_val = m_val
        return max_move



MAX_DEPTH=3
"""
Minimax recursive function
@author B Welsh
"""
def minimax(board, move, max_symbol, is_max=False, depth=0):
    # the symbol of the current player
    step_symbol=max_symbol if is_max else opposite_symbol(max_symbol)
    # build the current version of the board
    tmp_board = copy.deepcopy(board)
    tmp_board.make_move(step_symbol,move)
    # if the game would end
    if not tmp_board.game_continues():
        scores = tmp_board.calc_scores()
        if scores[max_symbol]>scores[opposite_symbol(max_symbol)]:
            return 20
        elif scores[max_symbol]<scores[opposite_symbol(max_symbol)]:
            return -20
        else:
            return 0

    moves=tmp_board.calc_valid_moves(step_symbol)

   # if not moves:
    #     # no valid moves
    #     return minimax(tmp_board,None,max_symbol,is_max,depth+1)
    # if depth is reached, run a version of greedy
    if depth>MAX_DEPTH:
        vals=[]
        for move in moves:
            m_val=len(tmp_board.is_valid_move(step_symbol,move))
            vals.append(m_val)
        if not vals:
            return 0
        if is_max:
            return max(vals)
        else:
            return -max(vals)

    # recursive case - search each move on the current board, and find the max/min
    vals=[]
    for move in moves:
        vals.append(minimax(tmp_board,move,max_symbol,not is_max,depth+1))
    if len(vals) is 0:
        return 0
    if is_max:
        return max(vals)
    else:
        return min(vals)




"""
Minimax player implementation
@author Kerry Buckman
"""
class MinimaxPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        valid_moves = board.calc_valid_moves(self.symbol) #all valid moves
        max_node = {} #dictionary of moves to their values

        #for each move, call minimax and get the evaluation
        #store in dictionary max node (key is move, value is value)
        for i in range(len(valid_moves)):
            board2 = copy.deepcopy(board)
            board2.make_move(self.symbol, valid_moves[i])
            move_val = self.minimax(board2, MAX_DEPTH, 1, False)
            max_node[tuple(valid_moves[i])] = move_val


        #find the node with the highest max val, return it
        max_val = max_node.get(tuple(valid_moves[0]))
        max_val_key = tuple(valid_moves[0]) # the key that matches with the highest value
        for x in max_node:
            if max_node.get(x) > max_val:
                max_val = max_node.get(x)
                max_val_key = x
        return max_val_key

    # returns value of a node (move)

    def minimax(self, board, max_depth, current_depth, my_turn):

        if my_turn == True:
            move_list = board.calc_valid_moves(self.symbol)

            if board.game_continues() == False:
                return self.eval_board(board)

            if current_depth == max_depth:  # deep as can go
                return self.eval_board(board)

            if len(move_list) == 0:  # end of tree or invalid move
                return self.minimax(board, max_depth, current_depth+1, False)

            values = set()
            for i in range(len(move_list)):
                board2 = copy.deepcopy(board)
                board2.make_move(self.symbol, move_list[i])
                val = self.minimax(board2, max_depth, current_depth + 1, False)
                values.add(val)

            return max(values)


        else:
            move_list = board.calc_valid_moves(board.get_opponent_symbol(self.symbol))

            if board.game_continues() == False:
                return self.eval_board(board)

            if current_depth == max_depth:    # deep as can go
                return self.eval_board(board)

            if len(move_list) == 0:  # end of tree or invalid move
                return self.minimax(board, max_depth, current_depth+1, True)

            values = set()
            for i in range(len(move_list)):
                board2 = copy.deepcopy(board)
                board2.make_move(board2.get_opponent_symbol(self.symbol), move_list[i])
                val = self.minimax(board2, max_depth, current_depth + 1, True)
                values.add(val)

            return min(values)






    #returns how many more pieces player 1 has than player 2
    def eval_board(self, board):
        scores = board.calc_scores()
        if self.symbol == "X":
            return scores.get("X")-scores.get("O")
        return scores.get("O")-scores.get("X")

