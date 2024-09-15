import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure


# makes a single histogram from a given data frame column
#   - data: pandas dataframe column to input into a histogram
#   - master: which frame of the gui to add the histogram to
#   - row: which row to add canvas to
#   - col: which column to add canvas to
def makeHistogram(data, master, row, col):
    fig = Figure(dpi=100)
    f = fig.gca() #gca = get current axes
    f.hist(data, bins=10)
    f.set_xlabel("x label")
    f.set_ylabel("y label")
    f.set_title("sample histogram: 'D'")
    fig.tight_layout()
    hist_canvas = FigureCanvasTkAgg(fig, master=master)
    hist_canvas.draw()
    hist_canvas.get_tk_widget().grid(row=row, column=col)


# returns the count of the highest bin
#   - data: pandas dataframe column 
def getHighestCount(data):
    hist = np.histogram(data)
    sizes = hist[0]
    return max(sizes)

