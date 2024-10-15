import numpy as np
import math
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure

filename = "FRETresult.dat"

class StackedHistMaker():

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

    def __init__(self, files, datacolumn, master, row, col, bins, title, x, y, color, edgecolor, edgewidth, xmax, xmin, ymax, ymin, xfontsize, yfontsize, shift=None):
        self.files = files
        self.datacolumn = datacolumn
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
        self.minlength = float('inf')

        self.makeStackedHistogram()

    def makeStackedHistogram(self):
        self.all_data = [] # list of dataframes
        min_data = 0
        max_data = 0
        min_length = float('inf')

        for file in self.files:
            path = file + "/" + filename
            data = self.get_eFRET_data(path)

            if len(data) < min_length:
                min_length = len(data)
            self.all_data.append(data)
            self.minlength = min_length

        #zeroes the data in each individual dataframe
        self.zero_data()

        # set number of bins
        if self.bins == 'Auto':
            self.bins = int(self.auto_bin())
        else:
            self.bins = int(self.bins)

        #create figure
        fig = Figure(dpi=80)
        axes = []
        for i in range(len(self.all_data)):
            ax = fig.add_subplot(len(self.all_data), 1, i+1)
            ax.hist(self.all_data[i][self.datacolumn], bins=self.bins, color=self.color, edgecolor=self.edgecolor, linewidth=self.edgewidth)
            axes.append(ax)
        
        #set up axis ticks, range, & scale
        for ax in axes:
            ax.sharey(axes[0])
            ax.set_xticks([])
            ax.set_xlim([self.xmin, self.xmax])
            ax.set_ylim([self.ymin, self.ymax]) 
            yticks = ax.yaxis.get_major_ticks()
            yticks[0].label1.set_visible(False) # this should probably be able to be toggled on & off
        axes[-1].xaxis.set_major_locator(plt.AutoLocator())


        #set axis titles
        axes[-1].set_xlabel(self.x, fontsize=self.xfontsize)
        fig.supylabel(self.y, fontsize=self.yfontsize)

        #set title & append figure to canvas
        fig.suptitle(self.title, y = 0.93)
        fig.subplots_adjust(wspace=0, hspace=0)
        hist_canvas = FigureCanvasTkAgg(fig, master=self.master)
        hist_canvas.draw()
        hist_canvas.get_tk_widget().grid(row=self.row, column=self.col)

    
    def getBins(self):
        return self.bins

    # returns dataframe from one file
    def get_eFRET_data(self, path):
        FRETresult = open(path, "r") 
        data = pd.read_fwf(FRETresult, header=None)
        data.columns = ["eFRET", "other"]
        return data

    # zeroes the first peak of the data
    #   - data: pandas df column
    #   - offset: how far to shift the data by
    def zero_data(self):
        # Make a histogram with two bins
        # so one bin in actual fret and the other is photobleaching
        zeroed_data = []
        for df in self.all_data:
            if self.offset == 'Auto':
                bin_edges = np.histogram(self.data, bins=2)[1]
                # divide the far edge of the first bin (photobleached) by 2 to get the midpoint
                self.offset = bin_edges[1] / 2
            elif self.offset == 'None':
                self.offset = 0.0
            # subtract that midpoint of from all of the eFRET data
            df[self.datacolumn] = df[self.datacolumn].astype(float)
            df[self.datacolumn] = df[self.datacolumn] - float(self.offset)
            zeroed_data.append(df)
        self.all_data = zeroed_data

    # returns the count of the highest bin
    #   - data: pandas dataframe column 
    def getHighestCount(data):
        hist = np.histogram(data)
        sizes = hist[0]
        return max(sizes)

    # calculates the number of bins based on size of dataset, using Sturges's Rule (log2n + 1) * 5
    #   - data: pandas dataframe column to input into a histogram
    def auto_bin(self):
        n = self.minlength
        logn = math.ceil(math.log2(n))
        return str(5*(logn + 1))
