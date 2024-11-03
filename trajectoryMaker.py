import numpy as np
import math
import pandas as pd
import matplotlib as plt 
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
import tkinter as tk

class TrajectoryMaker():

    # data should come in as a dataframe
    def __init__(self, data, master):
        self.data = data
        self.master = master

        self.fig = self.makeTrajectory()

    def makeTrajectory(self):
        fig = Figure(dpi=80)
        f = fig.gca()
        
        time = self.data["time"]
        donor = self.data["donor"]
        acceptor = self.data["acceptor"]

        f.plot(time, donor, color="lime", label="Donor")
        f.plot(time, acceptor, color="red", label="Acceptor")
        f.set_ylim([None, 500])
        f.legend()
        f.set_title("Intensity over Time")
        fig.tight_layout()
        
        trajectorycanvas = FigureCanvasTkAgg(fig, master=self.master)
        trajectorycanvas.draw()
        trajectorycanvas.get_tk_widget().grid(row=0, column=0)
        return fig