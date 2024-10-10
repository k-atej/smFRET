import numpy as np
import math
import pandas as pd
import matplotlib as plt
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
#   - edgecolor: color of bin edges in histogram
#   - edgecolor: linewidth of bin edges in histogram
#   - xmax: upper limit of x-axis
#   - xmin: lower limit of x-axis
#   - ymax: upper limit of y-axis
#   - ymin: lower limit of y-axis
#   - shift (optional): how much to shift the data by in order to zero the first column
def makeHistogram(data, master, row, col, bins, title, x, y, color, edgecolor, edgewidth, xmax, xmin, ymax, ymin, xfontsize, yfontsize, shift=None):
    #zero data points
    data = zero_data(data, shift)

    #create figure
    fig = Figure(dpi=80)
    f = fig.gca() #gca = get current axes

    # set number of bins
    if bins == 'Auto':
        bins = int(auto_bin(data))
    else:
        bins = int(bins)
    f.hist(data, bins=bins, color=color, edgecolor=edgecolor, linewidth=edgewidth)
    
    #set axis titles
    f.set_xlabel(x, fontsize=xfontsize)
    f.set_ylabel(y, fontsize=yfontsize)

    #set axis ranges, doesn't actually change the scale
    f.set_xlim([xmin, xmax])
    f.set_ylim([ymin, ymax])

    #set title & append figure to canvas
    f.set_title(title)
    fig.tight_layout()
    hist_canvas = FigureCanvasTkAgg(fig, master=master)
    hist_canvas.draw()
    hist_canvas.get_tk_widget().grid(row=row, column=col)
    return bins

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


# calculates the number of bins based on size of dataset, using Sturges's Rule (log2n + 1) * 5
#   - data: pandas dataframe column to input into a histogram
def auto_bin(data):
    n = data.count()
    logn = math.ceil(math.log2(n))
    print(str(logn + 1))
    return str(5*(logn + 1))
