# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy
import heapq


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



MAX_DEPTH=5
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
    def __init__(self, symbol, max_depth=12, ab_pruning=True):
        self.symbol = symbol
        self.max_depth=max_depth
        self.ab_pruning=ab_pruning

    def get_move(self, board):
        valid_moves = board.calc_valid_moves(self.symbol) #all valid moves
        max_node = {} #dictionary of moves to their values
        seen_boards = {} #transposition table: store board states and the value associated
        ab_val = 10000

        #for each move, call minimax and get the evaluation
        #store in dictionary max node (key is move, value is value)
        for i in range(len(valid_moves)):
            board2 = copy.deepcopy(board)
            board2.make_move(self.symbol, valid_moves[i])

            if(self.in_transposition_table(board2, seen_boards) == True): #already seen board state
                move_val = seen_boards[board2]
                ab_val = max(ab_val, move_val)
                max_node[tuple(valid_moves[i])] = move_val
            else: #if the board state hasn't been seen
                move_val = self.minimax(board2, self.max_depth, 1, False, seen_boards, ab_val)
                ab_val = max(ab_val, move_val)
                max_node[tuple(valid_moves[i])] = move_val
                seen_boards[board] = move_val
        # find the node with the highest max val, return it
        max_val = max_node.get(tuple(valid_moves[0]))
        max_val_key = tuple(valid_moves[0])  # the key that matches with the highest value
        for x in max_node:
            if max_node.get(x) > max_val:
                max_val = max_node.get(x)
                max_val_key = x
        return max_val_key

    # returns value of a node (move)


    def minimax(self, board, max_depth, current_depth, my_turn, seen_boards, parent_ab_val):
        if my_turn:
            move_list = board.calc_valid_moves(self.symbol)
            ab_val = 10000

            if not board.game_continues():
                return self.eval_board(board)

            if current_depth == max_depth:  # deep as can go
                return self.eval_board(board)

            if len(move_list) == 0:  # end of tree or invalid move
                return self.minimax(board, max_depth, current_depth + 1, False, seen_boards, ab_val)

            values = set()
            #beam_search_moves=self.beam_search(board,2,move_list)
            beam_search_moves=move_list
            for i in range(len(beam_search_moves)):
                board2 = copy.deepcopy(board)
                board2.make_move(self.symbol, beam_search_moves[i])
                if(self.in_transposition_table(board2, seen_boards) == True):
                    val = seen_boards[board2]
                else:
                    val = self.minimax(board2, max_depth, current_depth + 1, False, seen_boards, ab_val)
                # AB pruning
                # if one of our children is less than our parent's AB, then we'll pick it or worse,
                # and our parent node doesn't care about us
                # my we're a dysfunctional family
                if val>parent_ab_val and self.ab_pruning:
                    return val
                ab_val = max(ab_val, val)
                values.add(val)
                seen_boards[board] = val
            return max(values)


        else:
            move_list = board.calc_valid_moves(board.get_opponent_symbol(self.symbol))
            ab_val = -10000

            if not board.game_continues():
                return self.eval_board(board)

            if current_depth == max_depth:  # deep as can go
                return self.eval_board(board)

            if len(move_list) == 0:  # end of tree or invalid move
                return self.minimax(board, max_depth, current_depth + 1, True, seen_boards, ab_val)

            values = set()
            # beam_search_moves = self.beam_search(board, 2, move_list)
            beam_search_moves=move_list
            for i in range(len(beam_search_moves)):
                board2 = copy.deepcopy(board)
                board2.make_move(board2.get_opponent_symbol(self.symbol), move_list[i])

                if (self.in_transposition_table(board2, seen_boards) == True):
                    val = seen_boards[board2]
                else:
                    val = self.minimax(board2, max_depth, current_depth + 1, True, seen_boards, ab_val)
                    values.add(val)
                    seen_boards[board] = val
                board2.make_move(board2.get_opponent_symbol(self.symbol), beam_search_moves[i])
                if (self.in_transposition_table(board2, seen_boards) == True):
                    val = seen_boards[board2]
                else:
                    val = self.minimax(board2, max_depth, current_depth + 1, True, seen_boards, ab_val)
                    values.add(val)
                    seen_boards[board] = val
                # AB pruning
                # if one of our children is less than our parent's AB, then we'll pick it or worse,
                # and our parent node doesn't care about us
                # my we're a dysfunctional family
                if val<parent_ab_val and self.ab_pruning:
                    return val
                ab_val = min(ab_val, val)
                values.add(val)
                seen_boards[board] = val

            return min(values)


    def beam_search(self,board,n,possible_moves):
        if n>=len(possible_moves):
            return possible_moves
        else:
            moves_values_queue = []
            for move in possible_moves:
                board2 = copy.deepcopy(board)
                board2.make_move(self.symbol, move)
                value = self.eval_board(board)
                heapq.heappush(moves_values_queue, (value, move))
            best_moves = heapq.nlargest(n, moves_values_queue)
            best_moves_list = []
            for i in range(len(best_moves)):
                best_moves_list.append(best_moves[i][1])
            return best_moves_list



    #returns how many more pieces player 1 has than player 2
    def eval_board(self, board):
        scores = board.calc_scores()
        if self.symbol == "X":
            return scores.get("X")-scores.get("O")
        return scores.get("O")-scores.get("X")

    def in_transposition_table(self, board, seen_boards):
        #rotate and check all 4 possible perspectives
        #return true if it was already in the transposition table
        #false if it is new

        if (board in seen_boards): #actual state
            return True

        for i in range(3): #equivilant states
            board2 = copy.deepcopy(board)
            board2.rotate_board()
            #will currently check board from one perspective, rotate implementation next
            if(board2 in seen_boards):
                return True

        return False