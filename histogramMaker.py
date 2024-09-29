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
#   - title: graph title
#   - x: x-axis label
#   - y: y-axis label
#   - color: color of bins in histogram
#   - shift: how much to shift the data by in order to zero the first column
def makeHistogram(data, master, row, col, bins, title, x, y, color, shift=None):
    data = zero_data(data, shift)
    fig = Figure(dpi=60)
    f = fig.gca() #gca = get current axes
    f.hist(data, bins=bins, color=color)
    f.set_xlabel(x)
    f.set_ylabel(y)
    f.set_title(title)
    fig.tight_layout()
    hist_canvas = FigureCanvasTkAgg(fig, master=master)
    hist_canvas.draw()
    hist_canvas.get_tk_widget().grid(row=row, column=col)

# zeroes the first peak of the data
#   - data: pandas df column
#   - offset: how far to shift the data by
def zero_data(data, offset):
    # Make a histogram with two bins
    # so one bin in actual fret and the other is photobleaching
    if offset == 'Auto':
        bin_edges = np.histogram(data, bins=2)[1]
        # divide the far edge of the first bin (photobleached) by 2 to get the midpoint
        offset = bin_edges[1] / 2
    elif offset == 'None':
        offset = 0.0
    # subtract that midpoint of from all of the eFRET data
    data = data.astype(float)
    data = data - float(offset)
    print(f"Offset: {offset}")
    return data

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

