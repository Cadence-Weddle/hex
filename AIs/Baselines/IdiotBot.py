import random

'''
def idiot_move(game):
    return game.make_move(game.board[[x for x, j in enumerate([game.board]) if j == 0]
    [random.randint(0, len([x+1 for x, j in enumerate([game.board]) if j == 0]))]])
'''
#Simpler idiotbot
def idiot_move(game)
    return random.choice([x for x, item in enumerate(game.board) if item ==0])
    