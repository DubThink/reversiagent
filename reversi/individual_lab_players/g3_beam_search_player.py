# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy
import heapq



"""
Minimax player implementation
"""
class G3MinimaxPlayerBeamSearch:
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
            move_val = self.minimax(board2, 2, 1, False)
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

            if len(move_list) == 0:  # end of tree or invalid move
                return self.minimax(board, max_depth, current_depth+1, False)

            if current_depth == max_depth:  # deep as can go
                return self.eval_board(board)

            values = set()
            beam_search_moves=self.beam_search(board,2,move_list)
            #beam_search_moves=move_list
            for i in range(len(beam_search_moves)):
                board2 = copy.deepcopy(board)
                board2.make_move(self.symbol, beam_search_moves[i])
                val = self.minimax(board2, max_depth, current_depth + 1, False)
                values.add(val)

            return max(values)


        else:
            move_list = board.calc_valid_moves(board.get_opponent_symbol(self.symbol))

            if board.game_continues() == False:
                return self.eval_board(board)

            if len(move_list) == 0:  # end of tree or invalid move
                return self.minimax(board, max_depth, current_depth+1, True)

            if current_depth == max_depth:    # deep as can go
                return self.eval_board(board)

            values = set()
            beam_search_moves = self.beam_search(board, 2, move_list)
            #beam_search_moves=move_list
            for i in range(len(beam_search_moves)):
                board2 = copy.deepcopy(board)
                board2.make_move(board2.get_opponent_symbol(self.symbol), beam_search_moves[i])
                val = self.minimax(board2, max_depth, current_depth + 1, True)
                values.add(val)

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