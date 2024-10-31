import numpy as np
import math
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure

# name of the files to parse
filename = "FRETresult.dat"

savefilename = "FREThistogram_stacked.png"

# creates a stack of histograms to display in the stackedHistogramWindow
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

    def __init__(self, files, savepath, datacolumn, master, row, col, bins, title, titlefontsize, x, y, color, edgecolor, edgewidth, xmax, xmin, ymax, ymin, xfontsize, yfontsize, width, height, toggle, shift=None):
        self.files = files
        self.savepath = savepath
        self.datacolumn = datacolumn
        self.master = master
        self.row = row
        self.col = col
        self.bins = bins
        self.title = title
        self.titlesize = titlefontsize
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
        self.width = width
        self.height = height
        self.toggle = toggle

        self.fig = self.makeStackedHistogram()

    # generates the stack of histograms based on the parameters set in the customizability window
    def makeStackedHistogram(self):
        self.processData()

        #create figure
        fig = Figure(dpi=80)
        fig.set_figwidth(self.width)
        fig.set_figheight(self.height)
        axes = []
        for i in reversed(range(len(self.all_data_shifted))):
            ax = fig.add_subplot(len(self.all_data_shifted), 1, i+1)
            ax.hist(self.all_data_shifted[i][self.datacolumn], bins=self.bins, color=self.color, edgecolor=self.edgecolor, linewidth=self.edgewidth)
            axes.append(ax)
        
        #set up axis ticks, range, & scale
        for ax in axes:
            ax.sharey(axes[0])
            ax.set_xticks([])
            ax.set_xlim([self.xmin, self.xmax])
            ax.set_ylim([self.ymin, self.ymax]) 
            yticks = ax.get_yticklabels()
            if self.toggle == 1:
                yticks[0].set_visible(False)
    
        axes[0].xaxis.set_major_locator(plt.AutoLocator())

        for i in range(1, len(self.all_data_shifted)):
           axes[i].xaxis.set_major_locator(plt.AutoLocator())
           axes[i].set_xticklabels([])


        #set axis titles
        axes[0].set_xlabel(self.x, fontsize=self.xfontsize)
        fig.supylabel(self.y, fontsize=self.yfontsize, x = self.width / 50)
        
        
        #set title & append figure to canvas
        fig.suptitle(self.title, y = 0.93, x=0.57, fontsize=self.titlesize)
        fig.subplots_adjust(wspace=0, hspace=0, left=0.25, right=0.9)

        self.hist_canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.hist_canvas.draw()
        self.hist_canvas.get_tk_widget().grid(row=self.row, column=self.col)

        return fig

    # collects data from individual files, compiles them into a list of dataframes and sets the number of bins to use
    def processData(self):
        self.all_data = [] # list of dataframes
        min_length = float('inf')
        min_data = float('inf')
        max_data = 0

        for file in self.files:
            path = file + "/" + filename
            data = self.get_eFRET_data(path)

            if len(data) < min_length:
                min_length = len(data)
            if data["eFRET"].min() < min_data:
                min_data = data["eFRET"].min()
            if data["eFRET"].max() > max_data:
                max_data = data["eFRET"].max()
            self.all_data.append(data)
            self.minlength = min_length

        self.zero_data()

        # set number of bins
        if self.bins == 'Auto':
            self.bins = int(self.auto_bin())
            self.return_bins = self.bins
        elif float(self.bins) < 1:
            bin_width = float(self.bins)
            bins = np.arange(min_data, max_data + bin_width, bin_width)
            self.bins = bins 
            self.return_bins = len(bins) - 1
        else:
            self.bins = int(self.bins)
            self.return_bins = int(self.bins)


    # returns the number of bins used in a histogram
    def getBins(self):
        return self.return_bins

    # returns dataframe from one file
    def get_eFRET_data(self, path):
        FRETresult = open(path, "r") 
        data = pd.read_fwf(FRETresult, header=None)
        data.columns = ["eFRET", "other"]
        return data

    # zeroes the data in each dataframe generated; can shift by a designated value or do it automatically
    def zero_data(self):
        zeroed_data = []
        for df in self.all_data:
            if self.offset == 'Auto':
                # Make a histogram with two bins
                # so one bin in actual fret and the other is photobleaching
                bin_edges = np.histogram(self.data, bins=2)[1]
                # divide the far edge of the first bin (photobleached) by 2 to get the midpoint
                self.offset = bin_edges[1] / 2
            elif self.offset == 'None':
                self.offset = 0.0
            # subtract that midpoint of from all of the eFRET data
            df[self.datacolumn] = df[self.datacolumn].astype(float)
            df[self.datacolumn] = df[self.datacolumn] - float(self.offset)
            zeroed_data.append(df)
        self.all_data_shifted = zeroed_data

    # returns the count of the highest bin
    #   - data: pandas dataframe column 
    def getHighestCount(data):
        hist = np.histogram(data)
        sizes = hist[0]
        return max(sizes)

    # calculates the number of bins based on size of dataset, using Sturges's Rule (log2n + 1) * 5
    def auto_bin(self):
        n = self.minlength
        logn = math.ceil(math.log2(n))
        return str(5*(logn + 1))
    
    def save(self, refpath):
        self.fig.savefig(refpath)
        print("SAVED!")

    def destroy(self):
        self.hist_canvas.get_tk_widget().destroy()
