from tkinter import colorchooser, ttk
import pandas as pd
import tkinter as tk
from fileviewer.fileViewerMaker import *
import os

class FileViewerWindow(tk.Toplevel):
    def __init__(self, path, files): # path = user input file, files = keys 
        super().__init__()
        self.minsize(200, 200)
        self.df = []

        self.files = [] #list of files (not full paths!) found at the given path 
        for file in files:
            self.files.append(os.path.basename(file)) 

        self.filepaths = files #list of full file paths found at the given path
        self.numfiles = len(self.filepaths)

        self.index = 0
        self.trajectory = None

        self.savepath = path.rstrip("\\/")  #user input without final slashes
        self.titleset = os.path.basename(self.savepath) # folder set in the input path
        self.title(self.titleset)

        self.yshift = 0
        self.generation = 0

        self.dwellActive = False
        self.dwelltimedf = pd.DataFrame(columns=['Series', 'deltaT'])
        self.dwellseries = 0

        self.filepath = self.savepath
        self.type = '.csv'

        #full window 
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)

        #area above the intensity viewer
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

    def start(self):
        #self.makeFormat() #not visible, for now
        self.makeButtons()
        self.maketrajectory()
        #self.bind('<Return>', self.maketrajectory)
        self.bind('<BackSpace>', self.undo)
        self.bind('<Left>', self.back)
        self.bind('<Right>', self.next1)
        self.bind('<Return>', self.save)

        
    
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


    def dwellClicks(self):
        if self.dwellActive == False:
            self.updateDwellTable()
        else:
            self.tree = None
            for widget in self.subframeright.winfo_children():
                widget.destroy()
            self.dwellActive = False
            self.maketrajectory()

    def updateDwellTable(self, event=None):
        self.sub3togg.set(0)
        self.original_size = (self.winfo_width(), self.winfo_height())
        self.tree = ttk.Treeview(self.subframeright, show="headings")

        self.tree["columns"] = list(self.dwelltimedf.columns)
        self.tree.column("Series", anchor="center", width=50, stretch=False)
        self.tree.heading("Series", text="Series")
        self.tree.column("deltaT", anchor="center", width=250, stretch=False)
        self.tree.heading("deltaT", text="deltaT")

        for index, row in self.dwelltimedf.iterrows():
            self.tree.insert("", "end", values=list(row))

        # dwell time selection toggle
        self.toggledwell = tk.Checkbutton(self.subframeright, text="Click to Select Dwell Times", variable=self.dwelltogg, onvalue=1, offvalue=0)
        self.toggledwell.grid(row=0, column=0, padx=(10, 20), pady="10", columnspan=3)

        self.tree.grid(row=1, column=0, sticky="ew", padx=(10, 20), pady="10", columnspan=3)
        self.refreshButton = tk.Button(self.subframeright, text="Refresh", command=self.updateDwellTable)
        self.refreshButton.grid(row=2, column=0, sticky="ew", padx=(10,20), pady="10")

        self.seriesButton = tk.Button(self.subframeright, text="+ Series", command=self.addSeries)
        self.seriesButton.grid(row=2, column=1, sticky="ew", padx=(10,20), pady="10")

        self.seriesSaveButton = tk.Button(self.subframeright, text="Save", command=self.saveSeries)
        self.seriesSaveButton.grid(row=2, column=2, sticky="ew", padx=(10,20), pady="10")

        self.dwellActive = True
        self.dwellseries = self.trajectory.getDwellSeries()
        self.maketrajectory()

    def addSeries(self):
        self.trajectory.incrementDwellSeries()

    def makeFormat(self):
        self.tabControl = ttk.Notebook(master=self.subframerighttop)
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
        trajectories = open(self.filepaths[self.index], "r") 
        data = pd.read_fwf(trajectories, header=None)
        data.columns = ["time", "donor", "acceptor"]
        self.df = data

    def maketrajectory(self, event=None):
        if self.generation != 0:
            self.updateZero()
        self.generation += 1
        
        if self.trajectory is not None:
            self.trajectory.destroyWidget()
        self.get_data()

        title = self.filepaths[self.index]
        xfontsize = 12.0
        yfontsize = 12.0
        x2fontsize = 12.0
        y2fontsize = 12.0
        titlefontsize = 12.0

        summ = self.sumtogg.get() # on = 1

        self.trajectory = FileViewerMaker(title, self.titleset, self.df, self.subframeleft, "lime", 
                                          "red", "black", self.titleset, titlefontsize,
                                          "Time (s)", xfontsize, "Time (s)", x2fontsize, " ", yfontsize, 
                                          " ", y2fontsize, 4.5, 6.0, None, None, None, 
                                          None, None, None, 1, 1, 0,
                                          1, 1, self.yshift, self.sub3togg.get(), summ, 
                                          self.dwelltogg.get(), self.dwelltimedf, self.dwellseries)

        self.dwelltimedf = self.trajectory.getDwellData()
        self.dwellseries = self.trajectory.getDwellSeries()
        self.makeLabel()

    def back(self, event=None):
        self.index -= 1
        if self.index < 0:
            self.index = self.numfiles - 1
        self.trajectory.setShift(0.0)
        self.maketrajectory()

    def next1(self, event=None):
        self.index += 1
        if self.index >= self.numfiles:
            self.index = 0
        self.trajectory.setShift(0.0)
        self.maketrajectory()

    def makeLabel(self):
        self.label = tk.Label(self.subframetop, text=f"{self.index + 1} of {self.numfiles}")    
        self.label.grid(row=0, column=0, padx="10")

    def savewindow(self):
        self.win = tk.Toplevel()
        self.win.title("Set Filepath: ")
        self.unbind_all('<Return>')
        self.win.bind('<Return>', self.setfilepath)
        
        #input area for file name
        self.path_label = tk.Label(self.win, text="Save Filepath:")
        self.path_label.grid(row=0, column=0)
        self.ref_path = tk.StringVar(self.win)
        self.ref_path.set(self.filepath)

        self.combo6 = tk.Entry(self.win, textvariable=self.ref_path)
        self.combo6.config(width=50)
        self.combo6.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady="10")

        self.saveButton = tk.Button(self.win, text="SAVE", command=self.setfilepath)
        self.saveButton.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)
    
    def setfilepath(self, event=None):
        self.filepath = self.ref_path.get()
        self.type = ".csv"
        self.win.destroy()
        self.win.unbind_all('<Return>')
        self.bind('<Return>', self.save)
        
    def save(self, event=None):
        self.trajectory.save(self.filepath, self.type)
        self.next1()

    def updateZero(self, event=None):
        self.yshift = self.trajectory.getShift()

    def undo(self, event=None):
        if self.sub3togg.get() == 1:
            self.trajectory.setShift(0.0)
            self.trajectory.destroyWidget()
            self.maketrajectory()

    def saveSeries(self):
        self.win = tk.Toplevel()
        self.win.title("Save Dwell Time Data: ")
        self.unbind_all('<Return>')
        self.win.bind('<Return>', self.saveSeriesData)
        
        #input area for file name
        self.path_label = tk.Label(self.win, text="Save Filepath:")
        self.path_label.grid(row=0, column=0)
        self.ref_path = tk.StringVar(self.win)
        self.ref_path.set(self.filepath)

        self.combo6 = tk.Entry(self.win, textvariable=self.ref_path)
        self.combo6.config(width=50)
        self.combo6.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady="10")

        self.saveButton = tk.Button(self.win, text="SAVE", command=self.saveSeriesData)
        self.saveButton.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)

    
    def saveSeriesData(self, event=None):
        self.filepath = self.ref_path.get()
        self.type = ".csv"
        self.trajectory.saveDwellData(self.filepath, self.type)
        self.win.destroy()
        self.win.unbind_all('<Return>')
        self.bind('<Return>', self.save)