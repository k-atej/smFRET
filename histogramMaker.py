import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure



# makes a single histogram from a given data frame column
#   - data: pandas dataframe column to input into a histogram
#   - master: which frame of the gui to add the histogram to
#   - row: which row to add canvas to
#   - col: which column to add canvas to
#   - bins: number of bins for histogram to recognize
def makeHistogram(data, master, row, col, bins):
    fig = Figure(dpi=60)
    f = fig.gca() #gca = get current axes
    f.hist(data, bins=bins)
    f.set_xlabel("x label")
    f.set_ylabel("y label")
    f.set_title("______")
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

# returns an empty histogram
#   - master: which frame of the gui to add the histogram to
#   - row: which row to add canvas to
#   - col: which column to add canvas to
def emptyHistogram(master, row, col):
    df_empty = pd.DataFrame({'A' : []})
    fig = Figure(dpi=60)
    f = fig.gca() #gca = get current axes
    f.hist(df_empty, bins=10)
    f.set_xlabel(" ")
    f.set_ylabel(" ")
    f.set_title(" ")
    fig.tight_layout()

    hist_canvas = FigureCanvasTkAgg(fig, master=master)
    hist_canvas.draw()
    hist_canvas.get_tk_widget().grid(row=row, column=col)

