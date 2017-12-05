import numpy as np
import random
from time import time
import math
# Player 1 goes from top to bottom
# Player 2 goes from right to left


class HexGame:
    blank_board = np.zeros(121)
    default_players = [[1, "Player 1"], [2, "Player 2"]]
    default_starting_player = 0  # 0 for p1, 1 for p2
    default_state = 0
    default_log = True
    random_game_ID = random.randint(100000, 999999)
    default_winner_state = 0

    def __init__(self, gametick=0,
                 board=blank_board,
                 players=default_players,
                 log=default_log,
                 gameid =random_game_ID, winner_state=default_winner_state,
                 starting_player=default_starting_player):
        try:
            self.gametick = gametick
            self.board = board
            self.players = players
            self.log = log
            self.gameid = gameid
            self.winner_state = winner_state
            self.starting_player = starting_player
            self.history = []
            assert type(self.players) is list
            assert type(self.gametick) is int
            assert type(starting_player) is int and starting_player == 0 or 1
            if type(self.board) is list:
                self.board = np.array(self.board)
            assert type(board) is np.ndarray
            if self.log is True:
                with open(str(self.gameid) + ".hexlog", 'w') as log_file:
                    log_file.write("GameID:{}\n"
                                   "Player Names:{}\n"
                                   "Timestamp:{}\n"
                                   "LOG START:\n"
                                   .format(self.gameid, str(self.players[0][1])+","+str(self.players[1][1]), time()))
                    log_file.close()
        except AssertionError:
            raise TypeError
        print()

    def increment_gametick(self, value=1):
        self.gametick += value

    def set_game_tick(self, value):
        self.gametick = value

    def make_move(self, position):
        # Positions Start Counting From 1
        if self.board[position] == 0:
            np.put(self.board, position, self.players[self.gametick % 2+self.starting_player][0])
            self.gametick += 1
            self.winner_state = self.check_if_victory()
            self.history.append(position)
            if self.winner_state is not 0:
                print("GAME STATE AT {}".format(self.winner_state))
                return self.winner_state, self.gametick, self.board, position
        else:
            print("INVALID MOVE")
            if self.log is True:
                with open(str(self.gameid) + ".hexlog", 'a') as log_file:
                    log_file.write("INVALID MOVE BY PLAYER {}: Timestamp:{}\n"
                                   .format(self.players[(self.gametick+1) % 2][0], time()))
                    log_file.close()
            return "INVALID_MOVE"
        if self.log is True:
            self.log_move()

    def reset(self):
        self.gametick = 0
        self.board = np.zeros(121)
        self.winner_state = 0
        if self.log is True:
            with open(str(self.gameid) + ".hexlog", 'a') as log_file:
                log_file.write("GAME RESET Timestamp:{}\n".format(time()))
                log_file.close()

    def log_move(self):
        with open(str(self.gameid) + ".hexlog", 'a') as log_file:
            log_file.write("Gametick:{}\n"
                           "Timestamp:{}\n"
                           "Board:{}\n"
                           "Current Player Name:{}\n"
                           "Current Player Number:{}\n"
                           "Current State:{}\n"
                           "NEXT MOVE:\n"
                           .format(self.gametick, time(),
                                   self.board, self.players[self.gametick % 2+self.starting_player-1][0],
                                   self.players[self.gametick % 2 + self.starting_player-1][1],
                                   self.winner_state)
                           )
            log_file.close()

    def load_from_log(self, file, gametick):
        raise NotImplemented
    
    def generate_graph(self, values):
            cell_neighbor_weights = (1, 10, 11)  # Negatives are redundant
            graphs = []
            for value in values:
                for weight in cell_neighbor_weights:
                    if 0 <= value+weight <= 120:
                        in_graphs_flag = False
                        for independent_graph in graphs:
                            if value in set(independent_graph):
                                if value+weight not in set(independent_graph):
                                    independent_graph.extend([value+weight]) #May be causing redudant things to be appeneded to graph, or that may be mutiple checking of weights.
                                in_graphs_flag = True
                        if in_graphs_flag is False:
                            if value+weight in set(values):
                                graphs.append([value, value+weight])
                            else:
                                graphs.append([value])
            return graphs

    def check_if_victory(self):
        # Return 0 if No winner
        # Return 1 if winner is the first Player
        # Return 2 if winner is the second Player
        player_1_values = [x for x in range(len(self.board)) if self.board[x] == 1]
        player_2_values = [x for x in range(len(self.board)) if self.board[x] == 2]

        player_1_graphs = self.generate_graph(player_1_values)
        player_2_graphs = self.generate_graph(player_2_values)
        p1_side_1 = ([(11 * x) for x in range(11)])
        p1_side_2 = ([(11 * x)+10 for x in range(11)])
        p2_side_1 = ([x for x in range(11)])
        p2_side_2 = ([120 - x for x in range(11)])
        for graph in player_1_graphs:
            if len(set(p1_side_1).intersection(set(graph))) >= 1 and\
                            len(set(p1_side_2).intersection(set(graph))) >= 1:
                return 1
        for graph in player_2_graphs:
            if len(set(p2_side_1).intersection(set(graph))) >= 1 and\
                            len(set(p2_side_2).intersection(set(graph))) >= 1:
                return 2
        else:
            return 0

