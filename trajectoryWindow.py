import pandas as pd
import tkinter as tk
from histogramMaker import *
from histogramWindow import *
from stackedHistogramWindow import *
from trajectoryMaker import *
import os



class TrajectoryWindow(tk.Toplevel):
    def __init__(self, path, files):
        super().__init__()
        self.minsize(200, 200)
        self.df = []
        self.files = [] # name of final file
        for file in files:
            self.files.append(file.split("/")[-1])
        self.paths = files # full file path
        self.numfiles = len(self.paths)
        self.index = 0
        
        self.titleset = path.split("/")[-1] # final folder in the input path
        self.title(self.titleset)


        #full window 
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)

        #area above the intensity viewer
        self.subframetop = tk.Frame(self.frame, background='white')
        self.subframetop.grid(row=0, column=0, columnspan=2)

        # left half (contains intensities and efret figures)
        self.subframeleft = tk.Frame(self.frame, background='white')
        self.subframeleft.grid(row=1, column=0)

        # right half (contains menu)
        self.subframeright = tk.Frame(self.frame, background='white')
        self.subframeright.grid(row=1, column=1)

        self.start()

    def start(self):
        #self.makeFormat() not visible, for now
        self.makeButtons()
        self.maketrajectory()
        self.bind('<Left>', self.back)
        self.bind('<Right>', self.next1)
    
    def makeButtons(self):

        # generate button, bound to the generation of a histogram
        self.backbutton = tk.Button(self.subframetop, text="Back", command=self.back)
        self.backbutton.grid(row=0, column=1, padx="10")

        # clear button, bound to the generation of an empty histogram
        self.nextbutton = tk.Button(self.subframetop, text="Next", command=self.next1)
        self.nextbutton.grid(row=0, column=2, padx="10", pady="10")
    
    def makeFormat(self):
        self.tabControl = ttk.Notebook(master=self.subframeright)
        self.tabFormat = tk.Frame(self.tabControl)
        self.tabControl.grid(row=0, column=0, rowspan=2, padx=10, sticky='n')

        self.tabFormat = tk.Frame(self.tabControl)
        self.tabStyle = tk.Frame(self.tabControl)
        self.tabText = tk.Frame(self.tabControl)

        self.tabControl.add(self.tabFormat, text="Format")
        self.tabControl.add(self.tabStyle, text="Style")
        self.tabControl.add(self.tabText, text="Text")


    # parses the data file into a pandas dataframe
    def get_data(self):
        trajectories = open(self.paths[self.index], "r") 
        data = pd.read_fwf(trajectories, header=None)
        data.columns = ["time", "donor", "acceptor"]
        self.df = data

    def calculateEfret(self):
        gamma = 1
        self.df['efret'] = self.df['acceptor'] / (self.df['acceptor'] + (gamma * self.df['donor']))

    def maketrajectory(self):
        self.get_data()
        self.calculateEfret()
        title = self.paths[self.index]
        self.trajectory = TrajectoryMaker(title, self.titleset, self.df, self.subframeleft)
        self.makeLabel()

    def back(self, event=None):
        self.index -= 1
        if self.index < 0:
            self.index = self.numfiles - 1
        self.maketrajectory()


    def next1(self, event=None):
        self.index += 1
        if self.index >= self.numfiles:
            self.index = 0
        self.maketrajectory()

    def makeLabel(self):
        self.label = tk.Label(self.subframetop, text=f"{self.index + 1} of {self.numfiles}")    
        self.label.grid(row=0, column=0, padx="10")