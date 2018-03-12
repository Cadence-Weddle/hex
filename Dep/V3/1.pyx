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