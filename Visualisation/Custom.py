from PIL import Image, ImageTk
from tkinter import *
from tkinter.ttk import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import numpy as np


class GameBoardVisualization():
    @staticmethod
    def transform(matrix):
        #This is the most horrible way of doing this, can be cleaned up
        output = []
        for i in range(len(matrix)):
            out=[]
            out+=([-1 for _ in range(i)])
            for entry in matrix[i]:
                out.append(entry)
                out.append(entry)
            out+=([-1 for _ in range(10-i)])
            output.append(out)
            output.append(out)
        return output
    
    def __init__(self,master,matrix,dpi=500,cmap=None):
    
        self.master=master    
        self.dpi = dpi
        self.cmap = cmap
        
        self.board = Figure(dpi=self.dpi,frameon=False)
        self.board_plot = self.board.add_axes([0,0,1,1])
        self.board_plot.imshow(GameBoardVisualization.transform(matrix),cmap=self.cmap)
        self.board_plot.axis('off')
        self.canvas =  FigureCanvasTkAgg(self.board, master=self.master)
        
        
    def pack(self,**kwargs):
        self.canvas._tkcanvas.pack(kwargs)
        
    def update(self,matrix):
        self.board_plot.clear()
        self.board_plot.axis('off')
        self.board_plot.imshow(GameBoardVisualization.transform(matrix),cmap=self.cmap)
        self.canvas.draw()
        
        
class GameBoardVisualization2():
    @staticmethod
    def transform(matrix):
        #This is the most horrible way of doing this, can be cleaned up
        output = []
        for i in range(len(matrix)):
            out=[]
            out+=([-1 for _ in range(i)])
            for entry in matrix[i]:
                out.append(entry)
                out.append(entry)
            out+=([-1 for _ in range(10-i)])
            output.append(out)
            output.append(out)
        return output
    
    def __init__(self,master,matrix,dpi=500,cmap=None):
    
        self.master=master    
        self.dpi = dpi
        self.cmap = cmap
        plt.imsave('board.png',arr=GameBoardVisualization.transform(matrix),cmap=self.cmap)
        
        self.BoardImage = ImageTk.PhotoImage(Image.open("board.png"))
        self.board = Label(self, image=self.BoardImage)

    def pack(self, **kwargs):
        self.board.pack(kwargs)
    def update(self,matrix):
        plt.imsave('board.png',arr=GameBoardVisualization.transform(matrix),cmap=self.cmap)
        self.BoardImage = ImageTk.PhotoImage(Image.open("board.png"))
        self.board = Label(self, image=self.BoardImage)