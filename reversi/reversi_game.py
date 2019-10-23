# Written by Toby Dragon

import copy
from datetime import datetime

from reversi.player3.all_players import *
from reversi.reversi_board import ReversiBoard
from reversi.reversi_players import RandomComputerPlayer
from reversi.reversi_players import HumanPlayer

MAX_TIME=.5

class ReversiGame:

    def __init__(self, player1, player2, show_status=True, board_size=8):
        self.player1 = player1
        self.player2 = player2
        self.board = ReversiBoard(board_size)
        self.decision_times = {self.player1.symbol: 0, self.player2.symbol: 0}
        self.show_status = show_status
        self.play_game()

    def play_game(self):
        if self.show_status:
            self.board.draw_board()
        while self.board.game_continues():
            self.play_round()
        if self.show_status:
            print("Game over, Final Scores:")
            print_scores(self.board.calc_scores())

    def play_round(self):
        start = datetime.now()
        self.play_move(self.player1)
        dt=(datetime.now()-start).total_seconds()
        if dt>MAX_TIME:
            print(self.player1.symbol,"took",dt,"seconds.")
        self.decision_times[self.player1.symbol] +=dt
        start = datetime.now()
        self.play_move(self.player2)
        dt = (datetime.now() - start).total_seconds()
        if dt > MAX_TIME:
            print(self.player2.symbol, "took", dt, "seconds.")
        self.decision_times[self.player2.symbol] += dt

    def play_move(self, player):
        if self.board.calc_valid_moves(player.symbol):
            chosen_move = player.get_move(copy.deepcopy(self.board))
            if not self.board.make_move(player.symbol, chosen_move):
                print("Error: invalid move made")
            elif self.show_status:
                self.board.draw_board()
                print_scores(self.board.calc_scores())
        elif self.show_status:
            print(player.symbol, "can't move.")

    def calc_winner(self):
        scores = self.board.calc_scores()
        if scores[self.player1.symbol] > scores[self.player2.symbol]:
            return self.player1.symbol
        if scores[self.player1.symbol] < scores[self.player2.symbol]:
            return self.player2.symbol
        else:
            return "TIE"

    def get_decision_times(self):
        return self.decision_times


def print_scores(score_map):
    for symbol in score_map:
        print(symbol, ":", score_map[symbol], end="\t")
    print()


def compare_players(player1, player2, count=1):
    game_count_map = {player1.symbol: 0, player2.symbol: 0, "TIE": 0}
    time_elapsed_map = {player1.symbol: 0, player2.symbol: 0}
    for i in range(1, count+1):
        #if i % (count//10) == 0:
            #print(i, "games finished")
        # swap player order for unbiasing
        player1, player2 = player2, player1
        game = ReversiGame(player1, player2, show_status=False)
        print(game.calc_winner())
        game_count_map[game.calc_winner()] += 1
        decision_times = game.get_decision_times()
        for symbol in decision_times:
            time_elapsed_map[symbol] += decision_times[symbol]
    print(game_count_map)
    print(time_elapsed_map)


def main():
    # ReversiGame(FantasticPlayerWow("O"),MinimaxPlayerHowGreat("X"))
    #ReversiGame(MinimaxPlayer("X"), RandomComputerPlayer("O"), board_size=8)
    #ReversiGame(MinimaxPlayer("X"),RandomComputerPlayer("O"),board_size=4)
    # ReversiGame(MinimaxPlayer("O"),MinimaxPlayerHowGreat("X"))
    #for i in range(4,30):
    #    print("At depth %d:"%i)
    #    compare_players(MinimaxPlayerAB("O",i),MinimaxPlayer("X"),2)
    # compare_players(RandomComputerPlayer("O"),MinimaxPlayerHowGreat("X"),10)
    # ReversiGame(ReallyGreatPlayer("X"),GreedyComputerPlayer("O"))
    # compare_players(RandomComputerPlayer("X"), FantasticPlayerWow("O"))
    # compare_players(RandomComputerPlayer("X"), FantasticPlayerWow("O"))
    compare_players(get_combined_player("X"),get_player_b("O"),2)


if __name__ == "__main__":
    main()
