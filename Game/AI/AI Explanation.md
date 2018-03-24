# A Hex Playing Artifical Intelligence
## Introduction
Inspired by the paper, [Mastering the Game of Go Without Human Knowl](https://github.com/Cadence-Weddle/hex.github.io/blob/master/Game/static/Mastering%20the%20game%20of%20Go%20without%20human%20knowledge.pdf)

## Monte Carlo Tree Search
Monte Carlo Tree Search(MCTS) is a heurisitc search algorithm which seeks the way to find the best payoff for a game (represented by a game tree) though iterative random smapling.
### The Game Tree
To find the optimal move for a given senario, the game that is being played needs to be represented in a format that can be understood by an algorthim, which will traverse the tree to find the best move. A tree like structure (a directed graph) is created where the connections (edges) are player moves, which result in new board positions(nodes) and are connected to the move and thus the play before.
Each layer of edges represents a switch in players. When the game reaches a terminal state (a win/loss), a payoff (measured in utils) is given and this state is represented by a leaf node with no children.

![A game tree for Tic-Tac-Toe](https://upload.wikimedia.org/wikipedia/commons/d/da/Tic-tac-toe-game-tree.svg)

A game tree for Tic-Tac-Toe
### Traversing The Tree and Simple Tree Search
To find a good move to play, the tree search algorithm traverses the tree. Simple methods that can be used are mini-max, and alpha-beta tree search, however, these non-heuristic methods do not work well under problems with high branching factors, such as hex.

#### The Monte Carlo Method
The fundemental principle of the Monte Carlo method is that many interations of a random simulation will converge upon some point. Applied to Tree Search, the method is designed so that it will converge on promising moves.
Each node in the Monte Carlo Searh Tree has the following values:
    1. visit_count = 0        # N(s,a)
		2. mean_action_value = 0  # Q(s,a) || Acts as "score" it is what the MCTS considers.
		3. score = 0 #Neural network based evaluation | Ignores subnodes. 
		4. Expanded = False #Reached by MCTS search during the selection phase. 
		1prior_probability = prior_probability #Taken from the Parent node
		self.evaluation_function = UCT #Magic
		self.move = move #move required to take the game from the parent node's state to the current state.

Monte Carlo Tree Search follows a 4 step process:
1. Selection: Starting from some root node, successive child nodes are chosen by finding the most optimal points though the UCB1 heuristic (The maximum is chosen), the game tree expands towards that move.
2. Expansion, If said state is not a terminal state, create another child node and choose a node from one of those
3. Simulation: Play a random playout from the child node, or in this case, feed the game state data into the neural network network.
4. Backpropogation: Update the win/loss ratios for each of the nodes.

![Steps of Monte Carlo Tree Search](https://upload.wikimedia.org/wikipedia/commons/6/62/MCTS_%28English%29_-_Updated_2017-11-19.svg)

#### Scoring Methods and Multi-Armed Bandits
In this case

#### Rollout Policies

## Machine Learning

## Tying it Together

## Implementing the Logic for Hex

## Interacting with the AI
For more information about how the AI is presented, [click here](https://github.com/Cadence-Weddle/hex.github.io/blob/master/Game/Web%20Server%20and%20Frontend%20Explanation.md).
