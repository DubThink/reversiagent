
import random
import copy
import heapq

"""
Minimax player implementation
"""


class MinimaxPlayerG3:

    def __init__(self, symbol, max_depth=22, ab_pruning=True, transposition_table=True,beam_search_enabled=True,move_ordering_enabled=True):
        self.symbol = symbol
        self.max_depth=max_depth
        self.ab_pruning=ab_pruning
        self.transposition_table=transposition_table
        self.beam_search_enabled=beam_search_enabled
        self.move_ordering_enabled=move_ordering_enabled

    def get_move(self, board):
        # print('-'*10)
        valid_moves = board.calc_valid_moves(self.symbol) #all valid moves
        max_node = {} #dictionary of moves to their values
        seen_boards = {} #transposition table: store board states and the value associated
        ab_val = -10000

        #for each move, call minimax and get the evaluation
        #store in dictionary max node (key is move, value is value)
        for i in range(len(valid_moves)):
            board2 = copy.deepcopy(board)
            board2.make_move(self.symbol, valid_moves[i])

            if self.transposition_table and self.in_transposition_table(board2, seen_boards): #already seen board state
                move_val = seen_boards[board2]
                ab_val = max(ab_val, move_val)
                max_node[tuple(valid_moves[i])] = move_val
            else: #if the board state hasn't been seen
                move_val = self.minimax(board2, self.max_depth, 1, False, seen_boards, ab_val)
                ab_val = max(ab_val, move_val)
                max_node[tuple(valid_moves[i])] = move_val
                if self.transposition_table:
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
        # print(' '*current_depth+"*")
        if my_turn:
            move_list = board.calc_valid_moves(self.symbol)
            ab_val = -10000

            if not board.game_continues():
                return self.eval_board(board)

            if current_depth == max_depth:  # deep as can go
                return self.eval_board(board)

            if len(move_list) == 0:  # end of tree or invalid move
                return self.minimax(board, max_depth, current_depth + 1, False, seen_boards, ab_val)

            if self.beam_search_enabled:
                beam_search_moves=self.beam_search(board,5,move_list,self.symbol)
            elif self.move_ordering_enabled:
                beam_search_moves=self.beam_search(board,len(move_list),move_list,self.symbol)
            else:
                beam_search_moves=move_list
            # preallocate the list for speed
            values = [None]*len(beam_search_moves)
            for i in range(len(beam_search_moves)):
                board2 = copy.deepcopy(board)
                board2.make_move(self.symbol, beam_search_moves[i])
                if self.transposition_table and self.in_transposition_table(board2, seen_boards):
                    val = seen_boards[board2]
                else:
                    val = self.minimax(board2, max_depth, current_depth + 1, False, seen_boards, ab_val)
                # AB pruning
                # if one of our children is less than our parent's AB, then we'll pick it or worse,
                # and our parent node doesn't care about us
                # my we're a dysfunctional family
                if val > parent_ab_val and self.ab_pruning:
                    # print("pruned")
                    return val
                ab_val = max(ab_val, val)
                values[i]=val
                if self.transposition_table:
                    seen_boards[board] = val
            return max(values)


        else:
            move_list = board.calc_valid_moves(board.get_opponent_symbol(self.symbol))
            ab_val = 10000

            if not board.game_continues():
                return self.eval_board(board)

            if current_depth == max_depth:  # deep as can go
                return self.eval_board(board)

            if len(move_list) == 0:  # end of tree or invalid move
                return self.minimax(board, max_depth, current_depth + 1, True, seen_boards, ab_val)

            if self.beam_search_enabled:
                beam_search_moves=self.beam_search(board,2,move_list,board.get_opponent_symbol(self.symbol))
            elif self.move_ordering_enabled:
                beam_search_moves=self.beam_search(board,len(move_list),move_list,board.get_opponent_symbol(self.symbol))
            else:
                beam_search_moves=move_list

            # preallocate the list for speed
            values = [None] * len(beam_search_moves)
            for i in range(len(beam_search_moves)):
                board2 = copy.deepcopy(board)
                board2.make_move(board2.get_opponent_symbol(self.symbol), move_list[i])

                if self.transposition_table and self.in_transposition_table(board2, seen_boards):
                    # already seen board state
                    val = seen_boards[board2]
                else:
                    val = self.minimax(board2, max_depth, current_depth + 1, True, seen_boards, ab_val)
                # AB pruning
                # if one of our children is less than our parent's AB, then we'll pick it or worse,
                # and our parent node doesn't care about us
                # my we're a dysfunctional family
                if val < parent_ab_val and self.ab_pruning:
                    # print("pruned")
                    return val
                ab_val = min(ab_val, val)
                values[i] = val
                if self.transposition_table:
                    seen_boards[board] = val

            return min(values)


    def beam_search(self,board,n,possible_moves,symbol):
        if n>len(possible_moves):
            return possible_moves
        else:
            moves_values_queue = []
            for move in possible_moves:
                value=len(board.is_valid_move(symbol, move))
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

    def rotate(self, board):
        new_board = []
        row = []
        for i in range(len(board._board)):
            for j in range(len(board._board)):
                row.insert(0, board._board[j][i])
        new_board.append(row)

        board._board = new_board

    def in_transposition_table(self, board, seen_boards):
        #rotate and check all 4 possible perspectives
        #return true if it was already in the transposition table
        #false if it is new

        if board in seen_boards: #actual state
            print("WOWOWOWOW")
            return True

        board2 = copy.deepcopy(board)
        for i in range(3): #equivilant states
            self.rotate(board2)
            #will currently check board from one perspective, rotate implementation next
            if board2 in seen_boards:
                print("WLWWOWOWOWL")
                return True

        return False

def get_default_player(symbol):
    """
    :returns: a default minimax player that can operate successfully on a given 8x8 board
    """
    return MinimaxPlayerG3(symbol, ab_pruning=False, transposition_table=False, beam_search_enabled=False,move_ordering_enabled=False, max_depth=3)


def get_player_a(symbol):
    """
    :author: Kerry Buckman
    :enchancement: transposition table
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MinimaxPlayerG3(symbol, ab_pruning=False, transposition_table=True, beam_search_enabled=False, max_depth=3)


def get_player_b(symbol):
    """
    :author: Benjamin Welsh
    :enchancement: Alpha Beta pruning
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MinimaxPlayerG3(symbol, ab_pruning=True, transposition_table=False, beam_search_enabled=False,move_ordering_enabled=False,max_depth=3)


def get_player_c(symbol):
    """
    :author: Molly Noel
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MinimaxPlayerG3(symbol, ab_pruning=False, transposition_table=False, beam_search_enabled=True,max_depth=4)



def get_player_d(symbol):
    """
    :author: Molly Noel
    :enchancement:alpha beta pruning with move ordering
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MinimaxPlayerG3(symbol, ab_pruning=True, transposition_table=False, beam_search_enabled=False,move_ordering_enabled=True,max_depth=4)


def get_combined_player(symbol):
    """
    :returns: the best combination of the minimax enhancements that your team can create
    """
    return MinimaxPlayerG3(symbol,beam_search_enabled=True,transposition_table=False,move_ordering_enabled=True,max_depth=6)