import tkinter as tk
from histograms.histogramMaker import *
from histograms.histogramWindow import *
from histograms.stackedHistogramWindow import *
from histograms.histogramMain import *
from trajectories.trajectoryMain import *
from traceviewer.traceViewer import *
from distribution.distributionViewer import *
import os

#   /Users/katejackson/Desktop/Thrombin Aptamer/Apr15_11traces/(1) THROMBIN APTAMER, 0 mM KCl

# initializes and runs the application
def main():
    app = Application()
    app.mainloop()


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("smFRET Toolkit: Menu")
        self.buildMenu()

    # builds the start menu with options for the user to choose from: "Make Histograms" or "View Trajectories"
    def buildMenu(self):
        text_var = tk.StringVar()

        text_var.set("smFRET Toolkit:")
        welcome = tk.Label(self, textvariable=text_var)
        welcome.grid(column=0, row=0, sticky="nsew", padx=(50,50), pady=(40,10))

        self.chooseHists = tk.Button(self, text="Make Histograms", command=self.makeHistograms)
        self.chooseHists.grid(row=4, column=0, sticky="nsew", padx=(50, 50), pady=(20,40))

        self.chooseTraj = tk.Button(self, text="Make Trajectory Graphs", command=self.makeTrajectories)
        self.chooseTraj.grid(row=3, column=0, sticky="nsew", padx=(50, 50), pady=(20,10))

        self.chooseDist = tk.Button(self, text="View Distribution", command=self.viewDist)
        self.chooseDist.grid(row=2, column=0, sticky="nsew", padx=(50, 50), pady=(20,10))

        self.chooseTrace = tk.Button(self, text="View Traces", command=self.viewTrace)
        self.chooseTrace.grid(row=1, column=0, sticky="nsew", padx=(50, 50), pady=(20,10))

    # initializes a new histogram making window
    def makeHistograms(self):
        histogramHandler = HistogramMainApplication()

    # initializes a new trajectory making window
    def makeTrajectories(self):
        trajectoryHandler = TrajectoryMainApplication()

    # initializes a new distribution viewer
    def viewDist(self):
        distViewer = DistApplication()

    # initializes a new trace viewer
    def viewTrace(self):
        traceViewer = TraceApplication()


if __name__ == "__main__":
    main()