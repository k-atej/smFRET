from tkinter import colorchooser, ttk
import pandas as pd
import tkinter as tk
from fileviewer.fileViewerMaker import *
import os
import re

# easily modifiable parameters, all are cosmetic
XFONT = 12.0
YFONT = 12.0
X2FONT = 12.0
Y2FONT = 12.0
TITLEFONT = 12.0

DONORCOLOR = "lime"
ACCEPTORCOLOR = "red"
EFFICIENCYCOLOR = "black"

INTENSITY = 1
EFFICIENCY = 1
LEGEND = 0
SUBTITLE = 1
SUBTITLE2 = 1

# creates the window for viewing trace files as a tkinter toplevel
class FileViewerWindow(tk.Toplevel):
    
    # initializes the window for viewing files
    #   - path = user input file
    #   - files = keys: list of dataframes
    def __init__(self, path, files):
        super().__init__()
        self.minsize(200, 200)
        self.df = []
        self.files = files

        # list of files (not full paths!) found at the given path 
        #self.files = [] 
        #for file in files:
        #    self.files.append(os.path.basename(file)) 

        # list of full file paths found at the given path
        #self.filepaths = files 
        self.numfiles = len(self.files)
        
        # processing the user input to set the save path and the window title
        self.savepath = path.rstrip("\\/")  #user input without any final slashes
        self.tracenum = os.path.basename(self.savepath) # should be helx.traces
        self.tracenum = re.findall('\d+', self.tracenum)
        self.titleset = os.path.dirname(self.savepath) # last folder in file path
        self.savepath = self.titleset
        self.windowtitle = os.path.basename(self.titleset)
        print(f"trace: {self.tracenum}")
        self.title(self.windowtitle)

        # variables for tracking traces between generations
        self.index = 0
        self.trajectory = None
        self.yshift = 0
        self.generation = 0

        # dwell time analysis parameters
        self.dwellActive = False
        self.dwelltimedf = pd.DataFrame(columns=['Series', 'deltaT'])
        self.dwellseries = 0

        # variables initialized for saving the data
        self.filepath = self.savepath
        self.type = '.dat'

        # full window 
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)

        # area above the intensity viewer
        self.subframetop = tk.Frame(self.frame, background='white')
        self.subframetop.grid(row=0, column=0, columnspan=2)

        # left half (contains intensities and efret figures)
        self.subframeleft = tk.Frame(self.frame, background='white')
        self.subframeleft.grid(row=1, column=0, padx=(20, 0))

        # right half (contains menu)
        self.subframeright = tk.Frame(self.frame, background='white')
        self.subframeright.grid(row=1, column=1)

        # right half, top (contains i menu)
        self.subframerighttop = tk.Frame(self.subframeright, background='white')
        self.subframerighttop.grid(row=0, column=0)

        # right half, bottom (contains e menu)
        self.subframerightbottom = tk.Frame(self.subframeright, background='white')
        self.subframerightbottom.grid(row=1, column=0)

        self.start()

    # pastes the buttons/options onto the window and creates the trajectory
    # binds keys to various functions
    def start(self):
        self.makeButtons()
        self.maketrajectory()
        self.bind('<BackSpace>', self.undo)
        self.bind('<Left>', self.back)
        self.bind('<Right>', self.next1)
        self.bind('<Return>', self.save)

    # pastes the buttons/options onto the window and creates the trajectory 
    def makeButtons(self):
        # generate button, bound to the generation of a histogram
        makeTraj = tk.Button(self.subframetop, text="Regenerate", command=self.maketrajectory)
        makeTraj.grid(row=0, column=7, padx="10")

        # back button
        self.backbutton = tk.Button(self.subframetop, text="Back", command=self.back)
        self.backbutton.grid(row=0, column=1, padx="10")

        # next button
        self.nextbutton = tk.Button(self.subframetop, text="Next", command=self.next1)
        self.nextbutton.grid(row=0, column=2, padx="10", pady="10")
    
        # save button
        self.saveButton = tk.Button(self.subframetop, text="Set Filepath", command=self.savewindow)
        self.saveButton.grid(row=0, column=3, sticky="ew", padx="10", pady="10")

        # click-to-zero toggle
        self.sub3togg = tk.IntVar()
        self.togglesub3 = tk.Checkbutton(self.subframetop, text="Click to Zero", variable=self.sub3togg, onvalue=1, offvalue=0)
        self.togglesub3.grid(row=0, column=4, sticky="ew", padx="10", pady="10")
        self.sub3togg.set(0)

        # sum toggle
        self.sumtogg = tk.IntVar()
        self.togglesum = tk.Checkbutton(self.subframetop, text="Show Sum", variable=self.sumtogg, onvalue=1, offvalue=0)
        self.togglesum.grid(row=0, column=6, sticky="ew", padx="10", pady="10")
        self.sumtogg.set(0)

        # dwell time analysis button
        self.dwellButton = tk.Button(self.subframetop, text="Show Dwell Time Analysis", command=self.dwellClicks)
        self.dwellButton.grid(row=0, column=8, sticky="ew", padx="10", pady="10")
        self.dwelltogg = tk.IntVar()
        self.dwelltogg.set(0)

    # tracks the clicks made by the user on the window, related to the dwell time analysis
    def dwellClicks(self):
        if self.dwellActive == False:
            self.updateDwellTable()
        else:
            self.tree = None
            for widget in self.subframeright.winfo_children():
                widget.destroy()
            self.dwellActive = False
            self.maketrajectory()

    # creates the data table for the dwell time analysis shown on the window
    def updateDwellTable(self, event=None):
        # turn of click-to-zero
        self.sub3togg.set(0)

        # set up the tree in the side menu
        self.original_size = (self.winfo_width(), self.winfo_height())
        self.tree = ttk.Treeview(self.subframeright, show="headings")
        self.tree["columns"] = list(self.dwelltimedf.columns)
        self.tree.column("Series", anchor="center", width=50, stretch=False)
        self.tree.heading("Series", text="Series")
        self.tree.column("deltaT", anchor="center", width=250, stretch=False)
        self.tree.heading("deltaT", text="deltaT")

        # insert the values into the tree
        for index, row in self.dwelltimedf.iterrows():
            self.tree.insert("", "end", values=list(row))

        # dwell time selection toggle
        self.toggledwell = tk.Checkbutton(self.subframeright, text="Click to Select Dwell Times", variable=self.dwelltogg, onvalue=1, offvalue=0)
        self.toggledwell.grid(row=0, column=0, padx=(10, 20), pady="10", columnspan=3)

        # dwell time refresh button
        self.tree.grid(row=1, column=0, sticky="ew", padx=(10, 20), pady="10", columnspan=3)
        self.refreshButton = tk.Button(self.subframeright, text="Refresh", command=self.updateDwellTable)
        self.refreshButton.grid(row=2, column=0, sticky="ew", padx=(10,20), pady="10")

        # dwell time increment series button
        self.seriesButton = tk.Button(self.subframeright, text="+ Series", command=self.addSeries)
        self.seriesButton.grid(row=2, column=1, sticky="ew", padx=(10,20), pady="10")

        # dwell time save series data button
        self.seriesSaveButton = tk.Button(self.subframeright, text="Save", command=self.saveSeries)
        self.seriesSaveButton.grid(row=2, column=2, sticky="ew", padx=(10,20), pady="10")

        # save series data across trajectory generations
        self.dwellActive = True
        self.dwellseries = self.trajectory.getDwellSeries()
        self.maketrajectory()

    # increments the series value displayed in the chart by 1
    def addSeries(self):
        self.trajectory.incrementDwellSeries()

    # parses the data file into a pandas dataframe
    def get_data(self):
        data = self.files[self.index]
        #trajectories = open(self.filepaths[self.index], "r") 
        #data = pd.read_fwf(trajectories, header=None)
        #data.columns = ["time", "donor", "acceptor"]
        self.df = data

    # makes the trajectory to paste into the window 
    # by initializing a fileViewerMaker
    def maketrajectory(self, event=None):

        # if regenerating the trajectory, update the zeroed data
        # increment generation tracker
        if self.generation != 0:
            self.updateZero()
        self.generation += 1
        
        # if regenerating the trajectory, remove the previous trajectory
        if self.trajectory is not None:
            self.trajectory.destroyWidget()

        # retrieve the data to be displayed in the trajectory 
        self.get_data()

        # label the window with the filepath of the trajectory of interest
        title = f"Molecule {self.index + 1}"
        molnum = self.index + 1

        # check if the toggle for showing the sum is on
        summ = self.sumtogg.get() # on = 1

        # generate a trajectory with the FileViewerMaker class
        # see parameters in fileViewerMaker.py
        self.trajectory = FileViewerMaker(title, self.titleset, self.df, self.subframeleft, DONORCOLOR, 
                                          ACCEPTORCOLOR, EFFICIENCYCOLOR, title, TITLEFONT,
                                          "Time (s)", XFONT, "Time (s)", X2FONT, "I (A.U.)", YFONT, 
                                          "E", Y2FONT, 4.5, 6.0, INTENSITY, EFFICIENCY, LEGEND,
                                          SUBTITLE, SUBTITLE2, self.yshift, self.sub3togg.get(), summ, 
                                          self.dwelltogg.get(), self.dwelltimedf, self.dwellseries, 
                                          self.tracenum, molnum)

        # update dwell time data
        self.dwelltimedf = self.trajectory.getDwellData()
        self.dwellseries = self.trajectory.getDwellSeries()
        
        # generate label to add to top of window
        self.makeLabel()

    # return to previous trajectory
    # if used on first trajectory, will loop to last trajectory in list
    def back(self, event=None):
        self.index -= 1
        if self.index < 0:
            self.index = self.numfiles - 1
        self.trajectory.setShift(0.0)
        self.maketrajectory()

    # proceed to next trajectory
    # if used on last trajectory, will loop to first trajectory in list
    def next1(self, event=None):
        self.index += 1
        if self.index >= self.numfiles:
            self.index = 0
        self.trajectory.setShift(0.0)
        self.maketrajectory()

    # generate label displaying numerically which trajectory is being viewed
    def makeLabel(self):
        self.label = tk.Label(self.subframetop, text=f"{self.index + 1} of {self.numfiles}")    
        self.label.grid(row=0, column=0, padx="10")

    # creates a small window for user to enter the path to save the trajectories to
    # only needs to be set once, defaults to the same folder provided by the user
    #   when originally opening the data
    def savewindow(self):
        self.win = tk.Toplevel()
        self.win.title("Set Folder: ")

        # while this window is active, pressing "Enter" will set the save path
        # will revert once window is closed
        self.unbind_all('<Return>')
        self.win.bind('<Return>', self.setfilepath)
        
        #input area for file name, defaults to the path originally input by the user
        self.path_label = tk.Label(self.win, text="Save Folder:")
        self.path_label.grid(row=0, column=0)
        self.ref_path = tk.StringVar(self.win)
        self.ref_path.set(self.filepath)

        self.combo6 = tk.Entry(self.win, textvariable=self.ref_path)
        self.combo6.config(width=50)
        self.combo6.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady="10")

        # save button for the file path
        self.saveButton = tk.Button(self.win, text="SAVE", command=self.setfilepath)
        self.saveButton.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)

        # dropdown for designation of filetype
        reftype = ['.csv', '.dat']
        self.ref_type = tk.StringVar(self)
        self.ref_type.set('.dat')

        self.combo8 = tk.OptionMenu(self.win, self.ref_type, *reftype)
        self.combo8.config(width=5)
        self.combo8.grid(row=0, column=2, sticky="ew", padx=(0, 10), pady="10")
    
    # sets the user input into the save window as the path to which to save each trajectory
    def setfilepath(self, event=None):
        self.filepath = self.ref_path.get()
        self.type = self.ref_type.get()

        # close window and revert key binds
        self.win.destroy()
        self.win.unbind_all('<Return>')
        self.bind('<Return>', self.save)
        
    # save trajectory to specified filepath
    def save(self, event=None):
        self.trajectory.save(self.filepath, self.type)
        self.next1()

    # get shift data from trajectory
    # to be carried over to the next trajectory generation
    def updateZero(self, event=None):
        self.yshift = self.trajectory.getShift()

    # if click-to-zero is active, will set the zeroing to none
    # so displayed data is un-modified
    def undo(self, event=None):
        if self.sub3togg.get() == 1:
            self.trajectory.setShift(0.0)
            self.trajectory.destroyWidget()
            self.maketrajectory()

    # saves the dwell time data to a specified file path
    def saveSeries(self):
        # while this window is active, pressing "Enter" will set the save the data to the path
        # will revert once window is closed
        self.win = tk.Toplevel()
        self.win.title("Save Dwell Time Data: ")
        self.unbind_all('<Return>')
        self.win.bind('<Return>', self.saveSeriesData)
        
        #input area for full file name
        self.path_label = tk.Label(self.win, text="Save Filepath:")
        self.path_label.grid(row=0, column=0)
        self.ref_path = tk.StringVar(self.win)
        self.ref_path.set(self.filepath)

        self.combo6 = tk.Entry(self.win, textvariable=self.ref_path)
        self.combo6.config(width=50)
        self.combo6.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady="10")

        # save button for the dwell time data
        self.saveButton = tk.Button(self.win, text="SAVE", command=self.saveSeriesData)
        self.saveButton.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)

    # saves the series data to a csv
    # closes the window and reverts the key binds
    def saveSeriesData(self, event=None):
        self.filepath = self.ref_path.get()
        self.type = ".csv"
        self.trajectory.saveDwellData(self.filepath, self.type)
        self.win.destroy()
        self.win.unbind_all('<Return>')
        self.bind('<Return>', self.save)