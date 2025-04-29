import tkinter as tk
from histograms.histogramMaker import *
from histograms.histogramWindow import *
from histograms.stackedHistogramWindow import *
from histograms.histogramMain import *
from trajectories.trajectoryMain import *
import os

#   /Users/katejackson/Desktop/Thrombin Aptamer/Apr15_11traces/(1) THROMBIN APTAMER, 0 mM KCl

# initializes and runs the application
def main():
    app = Application()
    app.mainloop()


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.buildMenu()

    # builds the start menu with options for the user to choose from: "Make Histograms" or "View Trajectories"
    def buildMenu(self):
        text_var = tk.StringVar()
        text_var.set("Hello!")
        welcome = tk.Label(self, textvariable=text_var)
        welcome.grid(column=0, row=0, sticky="nsew", padx=(50,50), pady=(50,10))

        self.chooseHists = tk.Button(self, text="Make Histograms", command=self.makeHistograms)
        self.chooseHists.grid(row=1, column=0, sticky="nsew", padx=(50, 50), pady=(10,50))

        self.chooseTraj = tk.Button(self, text="View Trajectories", command=self.makeTrajectories)
        self.chooseTraj.grid(row=2, column=0, sticky="nsew", padx=(50, 50), pady=(10,50))

    # initializes a new histogram making window
    def makeHistograms(self):
        histogramHandler = HistogramMainApplication()

    # initializes a new trajectory making window
    def makeTrajectories(self):
        trajectoryHandler = TrajectoryMainApplication()


if __name__ == "__main__":
    main()