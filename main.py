import tkinter as tk
from histogramMaker import *
from histogramWindow import *
from stackedHistogramWindow import *
from histogramMain import *
from trajectoryMain import *
import os


def main():
    app = Application()
    app.mainloop()

# opens a small window. takes a file path and decides whether to open a histogram or stacked histogram window based on the number of eFRET_FILE_NAMEs found. 
class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.buildMenu()


    def buildMenu(self):
        text_var = tk.StringVar()
        text_var.set("Hello!")
        welcome = tk.Label(self, textvariable=text_var)
        welcome.grid(column=0, row=0, sticky="nsew", padx=(50,50), pady=(50,10))

        self.chooseHists = tk.Button(self, text="Make Histograms", command=self.makeHistograms)
        self.chooseHists.grid(row=1, column=0, sticky="nsew", padx=(50, 50), pady=(10,50))

        self.chooseTraj = tk.Button(self, text="View Trajectories", command=self.makeTrajectories)
        self.chooseTraj.grid(row=2, column=0, sticky="nsew", padx=(50, 50), pady=(10,50))


    def makeHistograms(self):
        histogramHandler = HistogramMainApplication()

    def makeTrajectories(self):
        trajectoryHandler = TrajectoryMainApplication()


if __name__ == "__main__":
    main()