import json
from libcpp cimport bool
from libc.time cimport time,time_t
import numpy as np
from cpython cimport array
cimport numpy as np
DTYPE = np.int
ctypedef np.int_t DTYPE_t


cdef class DefaultValues:
 # Player 1 goes from top to bottom
 # Player 2 goes from right to left
 cdef int starting_player,state,game_id
 cdef bool do_log
 cdef list log
 cdef tuple players
 cdef np.ndarray board
 board = np.zeros(121)
 players = ((1, "Player 1"), (2, "Player 2"))
 starting_player = 0  # 0 for p1, 1 for p2
 state = 0
 do_log = True
 game_id = int(time(NULL)*100)
 log = []

cdef class HexGame:
 def __init__(self,
     gametick=0,
     board=DefaultValues.board,
     players=DefaultValues.players,
     do_log=DefaultValues.do_log,
     game_id=DefaultValues.game_id,
     starting_player=DefaultValues.starting_player,
     log=DefaultValues.log,
     state=DefaultValues.state):
      
  # Initialising Instance Variables
  self.gametick = gametick
  self.board = np.array(board)
  self.players = players
  self.do_log = do_log
  self.game_id = game_id
  self.starting_player = starting_player
  self.log = log
  self.state = state
  # Type and Value Checking
  try:
   assert type(self.gametick) is int
   assert type(self.board) is np.ndarray
   assert type(self.players) is list and len(self.players) == 2
   assert self.do_log in (0,1)
   # No check for game ID
   assert self.starting_player in (0,1)
   assert self.history is list
   assert self.state in (0, 1, 2)

  except AssertionError:
   raise TypeError

  if self.do_log is True:
   self.history = self.history.append({'event': 'head',
            'game_id': self.game_id,
            'player_names': (self.players[0][1], self.players[1][1]),
            'timestamp': int(time(NULL))})
   self.update_log()

 def update_log(self):
  with open(str(self.game_id) + ".hexlog", 'w') as log_file:
   json.dump(self.history, log_file)
  log_file.close()

 cdef increment_gametick(self, int value=1):
  self.gametick += value

 def set_game_tick(self, value):
  self.gametick = value

 def make_move(self, position):
  if self.board[position] == 0:  # Board Position is Empty
   np.put(self.board, position, self.players[self.gametick % 2+self.starting_player][0])
   self.gametick += 1
   self.state = self.check_if_victory()
   self.history.append(position)
   if self.state is not 0:
    print("GAME STATE AT {}".format(self.state))
    return self.state, self.gametick, self.board
  else:
   print("invalid_move")
   if self.do_log is True:
     self.history = self.history.append({'event': 'invalid_move',
              'player': self.players[(self.gametick+1) % 2][0],
              'timestamp': int(time(NULL))})
     self.update_log()
   return "invalid_move"
  if self.do_log is True:
   self.history = self.history.append({'event': 'move',
            'timestamp': int(time(NULL)),
            'gametick': self.gametick,
            'board': self.board,
            'player_name':
            self.players[self.gametick % 2+self.starting_player-1][0],
            'player_number':
            self.players[self.gametick % 2 + self.starting_player-1][1],
            'state': self.state
            })
   self.update_log()

 def reset(self):
  self.gametick = 0
  self.board = np.zeros(121)
  self.state = 0
  self.history = self.history.append({'event': 'reset',
           'timestamp': int(time(NULL))})
  self.update_log()

 def load_from_log(self, file):
  self.history = json.load(file)
		


 @staticmethod
 #Going to try to rewrite this function is Pure C and interface with Python
 #-Jonathan Z. 12/3/2017 8:47 PM EST
 def generate_graph(values):
   cell_neighbor_weights = (1, 10, 11)  # Negatives are redundant
   graphs = []
   for value in values:
    for weight in cell_neighbor_weights:
     if 0 <= value+weight <= 120:
      in_graphs_flag = False
      for independent_graph in graphs:
       if value in independent_graph:
        if value+weight not in independent_graph:
         independent_graph.extend([value+weight])
        in_graphs_flag = True
      if in_graphs_flag is False:
       if value+weight in values:
        graphs.append([value, value+weight])
       else:
        graphs.append([value])
   return graphs

 def check_if_victory(self):
  # Return 0 if No winner
  # Return 1 if winner is the first Player
  # Return 2 if winner is the second Player
  p1_side_1 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
  p1_side_2 = (120, 119, 118, 117, 116, 115, 114, 113, 112, 111, 110)[::-1] 
  p2_side_1 = (0, 11, 22, 33, 44, 55, 66, 77, 88, 99, 110)      
  p2_side_2 = (10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110)    

  player_1_graphs = self.generate_graph(x for x in range(len(self.board)) if self.board[x] == 1)
  player_2_graphs = self.generate_graph(x for x in range(len(self.board)) if self.board[x] == 2)

  for graph in player_1_graphs:
   if graph[0] in p1_side_1 and graph[-1] in p1_side_2:
    return 1
   
  for graph in player_2_graphs:
   if graph[0] in p2_side_1 and graph[-1] in p2_side_2:
    return 2
  return 0

 def get_valid_moves(self):
  return [x for x, item in enumerate(self.board)]
	
	
