from tkinter import *
from Game.OLD.HexGame import HexGame

class Application(Frame):
    def __init__(self, master=None, **kwargs):
        Frame.__init__(master)
        self.master = master
        self.init_window()
        self.title = kwargs.get("title", "Python Hex Application")

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
        self.Player_1_menu.add_command(label="Human", command=self.set_player)

        self.Player_2_menu = Menu(menu)
        self.menu.add_cascade(label="Player 2", menu=self.Player_2_menu)

        self.Game_menu = Menu(menu)
        self.menu.add_cascade(label="Game", menu=self.Game_menu)

    def quit_app(self):
        exit(0)


if __name__=="__main__":
    root = Tk()
    app = Application(root)
    