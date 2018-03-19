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
To find a good move to play, the tree search algorithm

### The Monte Carlo Method

## Machine Learning

## Tying it Together

## Implementing the Logic for Hex

## Interacting with the AI
For more information about how the AI is presented, [click here](https://github.com/Cadence-Weddle/hex.github.io/blob/master/Game/Web%20Server%20and%20Frontend%20Explanation.md).
