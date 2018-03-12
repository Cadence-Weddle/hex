from .\Jonathan\model import model as jonathan_model
from .\Cadence\model import model as cadence_model
from HexGame import HexGame
from random import choice as choose

batches = int(input("Number of games to be played :~$")
Cadence = 0
Jonathan = 0



try:
    jonathan_model.move()
    jonathan_model.name
    cadence_model.move()
    cadence_model.name
except:
    raise Exception("Models do not comply with the arena regulations")



def play_game(model1, model2, log=False, print_data=True):
    game = HexGame(log=log)
    game_is_done = 0
    current_model = model1
    other_model = model2
    while not game_is_done:
        if print_data:
            print("Move {gametick}, {Models} Turn".format(gametick=game.gametick, Models=current_model.name))
        game_is_done, move = game.make_move(current_model.move(game))[0:-1:-1] #Returns win state and move made
        current_model, other_model = other_model, current_model
        if print_data:
            print("{Model} played in position {move}".format(Model=other_model.name, move=move))
    if print_data : ("Game is done. Winner:{}".format(game_is_done)
    return game_is_done, model1, model2
    
for i in range(batches):
    #do something
    
    
    
    