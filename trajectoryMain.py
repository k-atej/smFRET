import pandas as pd
import tkinter as tk
from histogramMaker import *
from histogramWindow import *
from stackedHistogramWindow import *
from trajectoryMaker import *
import os


#file name to look for results in, should probably be able to change this
#trajectory_search_name = "FRETresult.dat"

#example MacOS filepath
#path = "/Users/katejackson/Desktop/Thrombin Aptamer/Apr15_11 copy"

#def main():
 #   app = Application()
  #  app.mainloop()

# opens a small window. takes a file path and decides whether to open a histogram or stacked histogram window based on the number of eFRET_FILE_NAMEs found. 
class TrajectoryMainApplication(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Trajectory Viewer")
        self.minsize(200, 200)
        self.df = []
        self.path = "/Users/katejackson/Desktop/Thrombin Aptamer/Apr15_11traces/(1) THROMBIN APTAMER, 0 mM KCl/24 tr11.dat"

        self.get_data()
        self.trajectory()

    # parses the data file into a pandas dataframe
    def get_data(self):
        trajectories = open(self.path, "r") 
        data = pd.read_fwf(trajectories, header=None)
        data.columns = ["time", "donor", "acceptor"]
        self.df = data

    def trajectory(self):
        self.trajectory = TrajectoryMaker(self.df, self)
