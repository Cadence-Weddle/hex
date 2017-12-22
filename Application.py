from tkinter import *
from Game.OLD.HexGame import HexGame
from scipy.misc import imread

class Application(Frame):
    def __init__(self, master=None, **kwargs):
        Frame.__init__(master)
        self.master = master
        self.init_window()
        self.title = kwargs.get("title", "Python Hex Application")
        self.Player_1 = "Human"
        self.Player_2 = "Human"
        self.Player_Options = kwargs.get("Player_Options", ["Human", "Full_AlphaBeta", "Optimised_AlphaBeta"])


    def init_window(self):
        self.master.title(self.title)
        self.init_master_menu_bar()

    def init_master_menu_bar(self):
        menu = Menu(self.master)
        self.master.config(menu=menu)
        self.menu = menu
        self.menu.add_command(label="Quit", command=self.quit_app)

        self.Player_1_menu = Menu(menu)
        self.menu.add_cascade(label="Player 1", menu=self.Player_1_menu)
        self.Player_2_menu = Menu(menu)
        self.menu.add_cascade(label="Player 2", menu=self.Player_2_menu)

        for _ in self.Player_Options:
            self.Player_1_menu.add_command(label=_, command=self.set_player(1, _))
            self.Player_2_menu.add_command(label=_, command=self.set_player(2, _))

        self.Game_menu = Menu(menu)
        self.menu.add_cascade(label="Game", menu=self.Game_menu)


    def set_player(self, num, selection):
        def func(obj=self):
            setattr(obj, "Player_{}".format(num), selection)
        setattr(self, "Set_Player_{}_".format(num) + selection, func)
        return getattr(self, "Set_Player_{}_".format(num) + selection)



    def quit_app(self):
        exit(0)

    def update_game_board(self, location):
        self.img = imread(location)
        self.master










        

if __name__=="__main__":
    root = Tk()
    app = Application(root)
