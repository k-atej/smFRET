import numpy as np
import math
import pandas as pd
import matplotlib as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure

# creates a histogram to display in the histogramWindow
class HistMaker():

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

    def __init__(self, data, master, row, col, bins, title, x, y, color, edgecolor, edgewidth, xmax, xmin, ymax, ymin, xfontsize, yfontsize, shift=None):
        self.data = data
        self.master = master
        self.row = row
        self.col = col
        self.bins = bins
        self.title = title
        self.x = x
        self.y = y
        self.color = color
        self.edgecolor = edgecolor
        self.edgewidth = edgewidth
        self.xmax = xmax
        self.xmin = xmin
        self.ymax = ymax
        self.ymin = ymin
        self.xfontsize = xfontsize
        self.yfontsize = yfontsize
        self.offset = shift

        self.makeHistogram()


# makes a single histogram from a given data frame column
    def makeHistogram(self):
        self.zero_data()

        #create figure
        fig = Figure(dpi=80)
        f = fig.gca() #gca = get current axes

        # set number of bins
        if self.bins == 'Auto':
            self.bins = int(self.auto_bin())
        else:
            self.bins = int(self.bins)

        f.hist(self.data_shifted, bins=self.bins, color=self.color, edgecolor=self.edgecolor, linewidth=self.edgewidth)
        
        #set axis titles
        f.set_xlabel(self.x, fontsize=self.xfontsize)
        f.set_ylabel(self.y, fontsize=self.yfontsize)

        #set axis ranges, doesn't actually change the scale
        f.set_xlim([self.xmin, self.xmax])
        f.set_ylim([self.ymin, self.ymax])

        #set title & append figure to canvas
        f.set_title(self.title)
        fig.tight_layout()
        hist_canvas = FigureCanvasTkAgg(fig, master=self.master)
        hist_canvas.draw()
        hist_canvas.get_tk_widget().grid(row=self.row, column=self.col)
    
    #returns number of bins used in the histogram
    def getBins(self):
        return self.bins

    # zeroes the data in the dataframe; can shift by a designated value or do it automatically
    def zero_data(self):
        # Make a histogram with two bins
        # so one bin in actual fret and the other is photobleaching
        if self.offset == 'Auto':
            bin_edges = np.histogram(self.data, bins=2)[1]
            # divide the far edge of the first bin (photobleached) by 2 to get the midpoint
            self.offset = bin_edges[1] / 2
        elif self.offset == 'None':
            self.offset = 0.0
        # subtract that midpoint of from all of the eFRET data
        self.data = self.data.astype(float)
        self.data_shifted = self.data - float(self.offset)

    # returns the count of the highest bin
    #   - data: pandas dataframe column 
    def getHighestCount(data):
        hist = np.histogram(data)
        sizes = hist[0]
        return max(sizes)

    # calculates the number of bins based on size of dataset, using Sturges's Rule (log2n + 1) * 5
    def auto_bin(self):
        n = self.data.count()
        logn = math.ceil(math.log2(n))
        return str(5*(logn + 1))
