# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy

"""
Minimax player implementation
"""
class G3MinimaxPlayerABPruning:
    def __init__(self, symbol, max_depth=12, ab_pruning=True):
        self.symbol = symbol
        self.max_depth=max_depth
        self.ab_pruning=ab_pruning

    def get_move(self, board):
        valid_moves = board.calc_valid_moves(self.symbol)  # all valid moves
        max_node = {}  # dictionary of moves to their values
        ab_val = 10000
        # for each move, call minimax and get the evaluation
        # store in dictionary max node (key is move, value is value)
        for i in range(len(valid_moves)):
            board2 = copy.deepcopy(board)
            board2.make_move(self.symbol, valid_moves[i])
            move_val = self.minimax(board2, self.max_depth, 1, False,ab_val)
            ab_val=max(ab_val,move_val)
            max_node[tuple(valid_moves[i])] = move_val

        # find the node with the highest max val, return it
        max_val = max_node.get(tuple(valid_moves[0]))
        max_val_key = tuple(valid_moves[0])  # the key that matches with the highest value
        for x in max_node:
            if max_node.get(x) > max_val:
                max_val = max_node.get(x)
                max_val_key = x
        return max_val_key

    # returns value of a node (move)

    def minimax(self, board, max_depth, current_depth, my_turn, parent_ab_val):

        if my_turn:
            move_list = board.calc_valid_moves(self.symbol)
            ab_val = 10000

            if not board.game_continues():
                return self.eval_board(board)

            if current_depth == max_depth:  # deep as can go
                return self.eval_board(board)

            if len(move_list) == 0:  # end of tree or invalid move
                return self.minimax(board, max_depth, current_depth + 1, False, ab_val)

            values = set()
            for i in range(len(move_list)):
                board2 = copy.deepcopy(board)
                board2.make_move(self.symbol, move_list[i])
                val = self.minimax(board2, max_depth, current_depth + 1, False, ab_val)
                # AB pruning
                # if one of our children is less than our parent's AB, then we'll pick it or worse,
                # and our parent node doesn't care about us
                # my we're a dysfunctional family
                if val>parent_ab_val and self.ab_pruning:
                    return val
                ab_val = max(ab_val, val)
                values.add(val)

            return max(values)


        else:
            move_list = board.calc_valid_moves(board.get_opponent_symbol(self.symbol))
            ab_val = -10000

            if not board.game_continues():
                return self.eval_board(board)

            if current_depth == max_depth:  # deep as can go
                return self.eval_board(board)

            if len(move_list) == 0:  # end of tree or invalid move
                return self.minimax(board, max_depth, current_depth + 1, True, ab_val)

            values = set()
            for i in range(len(move_list)):
                board2 = copy.deepcopy(board)
                board2.make_move(board2.get_opponent_symbol(self.symbol), move_list[i])
                val = self.minimax(board2, max_depth, current_depth + 1, True, ab_val)
                # AB pruning
                # if one of our children is less than our parent's AB, then we'll pick it or worse,
                # and our parent node doesn't care about us
                # my we're a dysfunctional family
                if val<parent_ab_val and self.ab_pruning:
                    return val
                ab_val = min(ab_val, val)
                values.add(val)

            return min(values)

    # returns how many more pieces player 1 has than player 2
    def eval_board(self, board):
        scores = board.calc_scores()
        if self.symbol == "X":
            return scores.get("X") - scores.get("O")
        return scores.get("O") - scores.get("X")