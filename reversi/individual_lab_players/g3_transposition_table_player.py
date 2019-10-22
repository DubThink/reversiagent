# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy


"""
Minimax player implementation
"""
class G3MinimaxPlayerTranspositionTable:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        valid_moves = board.calc_valid_moves(self.symbol) #all valid moves
        max_node = {} #dictionary of moves to their values
        seen_boards = {} #transposition table: store board states and the value associated

        #for each move, call minimax and get the evaluation
        #store in dictionary max node (key is move, value is value)
        for i in range(len(valid_moves)):
            board2 = copy.deepcopy(board)
            board2.make_move(self.symbol, valid_moves[i])

            if(self.in_transposition_table(board2, seen_boards) == True): #already seen board state
                move_val = seen_boards[board2]
                max_node[tuple(valid_moves[i])] = move_val
            else: #if the board state hasn't been seen
                move_val = self.minimax(board2, 3, 1, False, seen_boards)
                max_node[tuple(valid_moves[i])] = move_val
                seen_boards[board] = move_val


        #find the node with the highest max val, return it
        max_val = max_node.get(tuple(valid_moves[0]))
        max_val_key = tuple(valid_moves[0]) # the key that matches with the highest value
        for x in max_node:
            if max_node.get(x) > max_val:
                max_val = max_node.get(x)
                max_val_key = x
        return max_val_key

    # returns value of a node (move)

    def minimax(self, board, max_depth, current_depth, my_turn, seen_boards):

        if my_turn == True:
            move_list = board.calc_valid_moves(self.symbol)

            if board.game_continues() == False:
                return self.eval_board(board)

            if len(move_list) == 0:  # end of tree or invalid move
                return self.minimax(board, max_depth, current_depth+1, False, seen_boards)

            if current_depth == max_depth:  # deep as can go
                return self.eval_board(board)

            values = set()
            for i in range(len(move_list)):
                board2 = copy.deepcopy(board)
                board2.make_move(self.symbol, move_list[i])

                if(self.in_transposition_table(board2, seen_boards) == True):
                    values.add(seen_boards[board2])
                else:
                    val = self.minimax(board2, max_depth, current_depth + 1, False, seen_boards)
                    values.add(val)
                    seen_boards[board] = val

            return max(values)


        else:
            move_list = board.calc_valid_moves(board.get_opponent_symbol(self.symbol))

            if board.game_continues() == False:
                return self.eval_board(board)

            if len(move_list) == 0:  # end of tree or invalid move
                return self.minimax(board, max_depth, current_depth+1, True, seen_boards)

            if current_depth == max_depth:    # deep as can go
                return self.eval_board(board)

            values = set()
            for i in range(len(move_list)):
                board2 = copy.deepcopy(board)
                board2.make_move(board2.get_opponent_symbol(self.symbol), move_list[i])

                if (self.in_transposition_table(board2, seen_boards) == True):
                    values.add(seen_boards[board2])
                else:
                    val = self.minimax(board2, max_depth, current_depth + 1, True, seen_boards)
                    values.add(val)
                    seen_boards[board] = val

            return min(values)



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

