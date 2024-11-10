import tkinter as tk
import glob
from histogramMaker import *
from histogramWindow import *
from stackedHistogramWindow import *
from trajectoryMaker import *
from trajectoryWindow import *
from stackedTrajectoryWindow import *
import os


#file name to look for results in, should probably be able to change this
#trajectory_search_name = "FRETresult.dat"

#example MacOS filepath
#path = "/Users/katejackson/Desktop/Thrombin Aptamer/Apr15_11 copy"

#def main():
 #   app = Application()
  #  app.mainloop()

class TrajectoryMainApplication(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Trajectory Menu")
        self.minsize(300, 200)

        #full window 
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)

        # start window
        self.subframe1 = tk.Frame(self.frame, background='white')
        self.subframe1.grid(row=0, column=0)

        #Title
        self.title_label = tk.Label(self.subframe1, text="Open A Folder:")
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=(10, 10), pady="10")

        #start button
        self.startButton = tk.Button(self.subframe1, text="START", command=self.onclick)
        self.startButton.grid(row=3, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)
        
        #input area for file path
        self.input_label = tk.Label(self.subframe1, text="File Path:")
        self.input_label.grid(row=1, column=0)
        self.ref_input = tk.StringVar(self)
        self.ref_input.set('')

        self.combo4 = tk.Entry(self.subframe1, textvariable=self.ref_input)
        self.combo4.config(width=30)
        self.combo4.grid(row=1, column=1, sticky="ew", padx=(10, 10), pady="10")

        # dropdown menu that allows selection of column in the dataframe, defaults to "eFRET," which is the first column
        self.choice_label = tk.Label(self.subframe1, text="View Type:")
        self.choice_label.grid(row=2, column=0)
        choices = ["Single", "Stacked"]
        self.ref_choice = tk.StringVar(self)
        self.ref_choice.set("Single")

        self.combo = tk.OptionMenu(self.subframe1, self.ref_choice, *choices)
        self.combo.config(width=10)
        self.combo.grid(row=2, column=1, sticky="w", padx=10)

    def onclick(self):
        keys = self.processPath()
        #print(keys)
        if self.ref_choice.get() == "Single":
            trajectory_window = TrajectoryWindow(self.ref_input.get(), keys)
        elif self.ref_choice.get() == "Stacked":
            stackedtrajectory_window = stackedTrajectoryWindow(self.ref_input.get(), keys)

    def processPath(self):
        filepath = self.ref_input.get()
        #print(filepath)
        filetype = '* tr*.dat'
        keys = []
        for root, dirs, files in os.walk(filepath):
            dirs.sort()
            files.sort()
            for file in files:
                if glob.fnmatch.fnmatch(file, filetype):
                    keys.append(os.path.join(root, file))
        return keys

        

