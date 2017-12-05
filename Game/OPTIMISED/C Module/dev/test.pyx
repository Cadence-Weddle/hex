import numpy as np
cimport numpy as np
DTYPE = np.int
ctypedef np.int_t DTYPE_t
from libcpp cimport bool
from libc.time cimport time,time_t

cdef class DefaultValues:
      # Player 1 goes from top to bottom
      # Player 2 goes from right to left
      cdef int starting_player,state,game_id
      cdef bool do_log
      cdef list log
      cdef np.ndarray board
      board = np.zeros(121)
      players = np.chararray( [[1, "Player 1"], [2, "Player 2"]])
      starting_player = 0  # 0 for p1, 1 for p2
      state = 0
      do_log = True
      game_id = int(time(NULL)*100)
      log = []