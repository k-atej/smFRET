import pandas as pd
import tkinter as tk
from histogramMaker import *
from histogramWindow import *
from stackedHistogramWindow import *
from trajectoryMaker import *




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

        self.savepath = path.rstrip("/")
        print(self.savepath)
        
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
    
        # save button
        self.saveButton = tk.Button(self.subframetop, text="Save", command=self.savewindow)
        self.saveButton.grid(row=0, column=3, sticky="ew", padx="10", pady="10")

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

    def savewindow(self):
        self.win = tk.Toplevel()
        self.win.title("Set Filepath: ")
        
        #input area for file name
        self.path_label = tk.Label(self.win, text="Save File Path:")
        self.path_label.grid(row=0, column=0)
        self.ref_path = tk.StringVar(self.win)
        self.ref_path.set(self.savepath)

        self.combo6 = tk.Entry(self.win, textvariable=self.ref_path)
        self.combo6.config(width=50)
        self.combo6.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady="10")

        # dropdown for designation of filetype
        reftype = ['.pdf', '.png', '.svg', '.ps', '.eps']
        self.ref_type = tk.StringVar(self)
        self.ref_type.set('.png')

        self.combo8 = tk.OptionMenu(self.win, self.ref_type, *reftype)
        self.combo8.config(width=5)
        self.combo8.grid(row=0, column=2, sticky="ew", padx=(0, 10), pady="10")

        # dropdown for designation of file quality
        self.qual_label = tk.Label(self.win, text="Quality:")
        self.qual_label.grid(row= 1, column=0)
        refqual = ["Low", "Medium", "High"]
        self.ref_qual = tk.StringVar(self)
        self.ref_qual.set('Medium')

        self.combo9 = tk.OptionMenu(self.win, self.ref_qual, *refqual)
        self.combo9.config(width=5)
        self.combo9.grid(row=1, column=1, sticky="w", padx=(0, 10), pady="10")


        self.saveButton = tk.Button(self.win, text="SAVE", command=self.save)
        self.saveButton.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)
        #self.win.mainloop()
    
    def save(self):
        self.trajectory.save(self.ref_path.get(), self.ref_type.get(), self.ref_qual.get())
        self.win.destroy()