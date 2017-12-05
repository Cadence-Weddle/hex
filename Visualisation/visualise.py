from imageio import imread, imwrite
import numpy as np
import selenium
#from http.server import BaseHTTPRequestHandler, HTTPServer #Uneccessary unless we want to implement multiple users playing ai's at a time.
 

def gen_start_image(location):
    img = imread(open(location))
    return im
    
class Visualiser():
    def __init__(game, location="Resources\\background.png")
        self.game = game
        self.write_location = "temp\\current_background.png"
        self.background = imread(location)
        self.image = self.background


    def update(self):
        out_image = self.image
        curr_player self.game.gametick % 2 + 1
        player_hexagon = imread("player_{num}_hexagon.png".format(num=curr_player)
        