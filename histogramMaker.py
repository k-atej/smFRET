import numpy as np
import math
import pandas as pd
import matplotlib as plt 
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
import tkinter as tk


#should be able to change this
savefilename = "FREThistogram.png"


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

    def __init__(self, data, savepath, master, row, col, bins, bin1, title, titlefontsize, x, y, color, edgecolor, edgewidth, xmax, xmin, ymax, ymin, xfontsize, yfontsize, width, height, annotations, shift=None):
        self.data = data
        self.savepath = savepath
        self.master = master
        self.row = row
        self.col = col
        self.bins = bins
        self.bintype = bin1
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
        self.width = width
        self.height = height
        self.annotations = annotations

        self.fig = self.makeHistogram()


# makes a single histogram from a given data frame column
    def makeHistogram(self):
        self.zero_data()

        #create figure
        fig = Figure(dpi=80)
        fig.set_figwidth(self.width)
        fig.set_figheight(self.height)
        f = fig.gca() #gca = get current axes
        
        # set number of bins
        if self.bins != 'Auto':
            if 'Auto' in str(self.bins):
                self.bins = 'Auto'
            elif float(self.bins) < 1.0:
                if self.bintype == 0:
                    self.bins = 'Auto'
        if self.bins == 'Auto':
            if self.bintype == 0:
                self.bins = int(self.auto_bin())
                self.return_bins = f'Auto:{self.bins}'
            else:
                bin_width = float(self.auto_bin_width())
                bins = np.arange(min(self.data), max(self.data) + bin_width, bin_width)
                self.bins = bins 
                self.return_bins = bin_width
        elif self.bintype == 1:
            bin_width = float(self.bins)
            bins = np.arange(min(self.data), max(self.data) + bin_width, bin_width)
            self.bins = bins 
            self.return_bins = bin_width
        else:
            self.bins = int(self.bins)
            self.return_bins = int(self.bins)

        f.hist(self.data_shifted, bins=self.bins, color=self.color, edgecolor=self.edgecolor, linewidth=self.edgewidth)
        
        #set axis titles
        f.set_xlabel(self.x, fontsize=self.xfontsize)
        f.set_ylabel(self.y, fontsize=self.yfontsize)

        #set axis ranges, doesn't actually change the scale
        f.set_xlim([self.xmin, self.xmax])
        f.set_ylim([self.ymin, self.ymax])

        self.xlim = f.get_xlim()
        self.ylim = f.get_ylim()

        #set title & append figure to canvas
        f.set_title(self.title, fontsize=self.titlesize)
        fig.tight_layout()
        self.hist_canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.hist_canvas.draw()
        self.hist_canvas.get_tk_widget().grid(row=self.row, column=self.col)

        if len(self.annotations) != 0:
            for annotation in self.annotations:
                self.draw_annotations(f, annotation)

        fig.canvas.mpl_connect('button_press_event', lambda event: self.onclick(event, self.hist_canvas))

        return fig
    
    #returns number of bins used in the histogram
    def getBins(self):
        return self.return_bins
    
    def getAnnotations(self):
        return self.annotations

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

    def auto_bin_width(self):
        hist, bin_edges = np.histogram(self.data_shifted)
        binwidths = bin_edges[1] - bin_edges[0]
        return binwidths

    def save(self, refpath):
        self.fig.savefig(refpath, dpi=200)
        self.annotate(refpath)
        print("SAVED!")

    def destroy(self):
        self.hist_canvas.get_tk_widget().destroy()

    def annotate(self, refpath):
        text = self.getText()
        refpath = refpath.split(".")[:-1]
        pathway = ""
        for path in refpath:
            pathway += path
        path = str(pathway) + ".txt"
        f = open(path, "w")
        f.write(text)

    def getText(self):
        # if bintype = 1, bin width; otherwise bin number
        if self.bintype == 1:
            binny = "bin width"
        elif self.bintype == 0:
            binny = "bin number"
        
        xmin, xmax = self.xlim
        ymin, ymax = self.ylim

        text = f"""
        data: {self.data}
        savepath: {self.savepath}
        bins: {self.bins}
        bintype: {binny}
        title: {self.title}
        title fontsize: {self.titlesize}
        x-axis label: {self.x}
        y-axis label: {self.y}
        fill color: {self.color}
        edge color: {self.edgecolor} 
        edge width: {self.edgewidth}
        x-axis max: {xmax}
        x-axis min: {xmin}
        y-axis max: {ymax}
        y-axis min: {ymin}
        x-axis label fontsize: {self.xfontsize}
        y-axis label fontsize: {self.yfontsize}
        offset: {self.offset}
        figure width: {self.width}
        figure height: {self.height} 

        """
        return text
    
    # 'clear' button removes annotations
    def onclick(self, event, canvas):
        if event.inaxes:
            x = event.xdata
            self.draw_annotations(event.inaxes, x)
            self.annotations.append(x)
            #print(self.annotations)
    
    def draw_annotations(self, axis, x):
        canvas = self.hist_canvas
        ymin, ymax = self.ylim
        axis.annotate('', xy=(x, 0), xytext=(x, ymax), xycoords='data', arrowprops=dict(arrowstyle='-', color='red', linestyle="dashed"))
        canvas.draw()
        




