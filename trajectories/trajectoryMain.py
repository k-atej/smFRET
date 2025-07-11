import tkinter as tk
import glob
from histograms.histogramMaker import *
from histograms.histogramWindow import *
from histograms.stackedHistogramWindow import *
from trajectories.trajectoryMaker import *
from trajectories.trajectoryWindow import *
from trajectories.stackedTrajectoryWindow import *
import os


#example MacOS filepath
#path = "/Users/katejackson/Desktop/Thrombin Aptamer/Apr15_11traces/(3) THROMBIN APTAMER, 20 mM KCl"

FILETYPE = '* tr*' 

# creates a window for inputting the path to a folder containing trace files
class TrajectoryMainApplication(tk.Toplevel):
    # initalize the window
    def __init__(self):
        super().__init__()
        self.title("Make Trajectory Graphs")
        self.minsize(300, 200)

        #full window 
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)

        # start window
        self.subframe1 = tk.Frame(self.frame, background='white')
        self.subframe1.grid(row=0, column=0)

        #Title
        self.title_label = tk.Label(self.subframe1, text="Open a folder of single trajectory files:")
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=(10, 10), pady="10")

        #start button
        self.startButton = tk.Button(self.subframe1, text="START", command=self.onclick)
        self.startButton.grid(row=4, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)
        
        #input area for file path
        self.input_label = tk.Label(self.subframe1, text="Path:")
        self.input_label.grid(row=1, column=0)
        self.ref_input = tk.StringVar(self)
        self.ref_input.set('')

        self.combo4 = tk.Entry(self.subframe1, textvariable=self.ref_input)
        self.combo4.config(width=30)
        self.combo4.grid(row=1, column=1, sticky="ew", padx=(10, 10), pady="10")

        # dropdown for designation of filetype (either csv or dat)
        self.type_label = tk.Label(self.subframe1, text="File types:")
        self.type_label.grid(row=2, column=0)

        reftype = ['.csv', '.dat']
        self.ref_type = tk.StringVar(self)
        self.ref_type.set('.dat')

        self.combo8 = tk.OptionMenu(self.subframe1, self.ref_type, *reftype)
        self.combo8.config(width=5)
        self.combo8.grid(row=2, column=1, sticky="ew", padx=(10, 10), pady="10")

        # dropdown menu that allows selection of column in the dataframe, defaults to "eFRET," which is the first column
        self.choice_label = tk.Label(self.subframe1, text="View type:")
        self.choice_label.grid(row=3, column=0)
        choices = ["Single", "Stacked"]
        self.ref_choice = tk.StringVar(self)
        self.ref_choice.set("Single")

        self.combo = tk.OptionMenu(self.subframe1, self.ref_choice, *choices)
        self.combo.config(width=10)
        self.combo.grid(row=3, column=1, sticky="w", padx=10)

    # when the button is clicked, the program looks for the number of traces to graph
    # if the option is set to single, initializes a single view
    # otherwise it initializes a stacked view
    def onclick(self):
        keys, filetype = self.processPath()
        if self.ref_choice.get() == "Single":
            trajectory_window = TrajectoryWindow(self.ref_input.get(), keys, filetype)
        elif self.ref_choice.get() == "Stacked":
            stackedtrajectory_window = stackedTrajectoryWindow(self.ref_input.get(), keys, filetype)
    
    # combs through given folder and finds all files matching the designate filetype
    def processPath(self):
        filepath = self.ref_input.get()
        filetype = FILETYPE + self.ref_type.get()
        keys = []
        for root, dirs, files in os.walk(filepath):
            dirs.sort()
            files.sort()
            for file in files:
                if glob.fnmatch.fnmatch(file, filetype):
                    keys.append(os.path.join(root, file))
        return keys, filetype

        

