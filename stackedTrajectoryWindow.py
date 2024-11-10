import pandas as pd
import tkinter as tk
from histogramMaker import *
from histogramWindow import *
from stackedHistogramWindow import *
from trajectoryMaker import *
from stackedTrajectoryMaker import *



class stackedTrajectoryWindow(tk.Toplevel):
    def __init__(self, path, files):
        super().__init__()
        self.minsize(200, 200)
        self.path = path  # what the user input into the box in the menu
        self.files = files  # list of filepaths for every trace file found within the folder
        self.figtitle = self.path.split("/")[-1]
        self.title(self.figtitle)

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
        self.maketrajectory()
    
    
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


    # HOW DO I NEED TO RESTRUCTURE THIS?

    # parses the files into a series of pandas dataframes
    def get_data(self):
        self.all_data = []
        for file in self.files:
            trajectory = open(file, "r") 
            data = pd.read_fwf(trajectory, header=None)
            data.columns = ["time", "donor", "acceptor"]
            self.all_data.append(data)

    def calculateEfret(self):
        for data in self.all_data:
            gamma = 1
            data['efret'] = data['acceptor'] / (data['acceptor'] + (gamma * data['donor']))

    def maketrajectory(self):
        self.get_data()
        self.calculateEfret()
        #title = self.paths[self.index]
        self.trajectory = StackedTrajectoryMaker(self.all_data, self.subframeleft, self.figtitle)
    