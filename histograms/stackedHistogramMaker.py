import numpy as np
import math
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
import os

# creates a stack of histograms to display in the stackedHistogramWindow
#   - files: files from which to pull data
#   - savepath: what to set as the default save path
#   - filename: name of the file that we were searching for
#   - datacolumn: pandas dataframe column to input into histograms
#   - master: which frame of the gui to add the histogram to
#   - row: which row to add canvas to
#   - col: which column to add canvas to
#   - bins: number of bins for histogram to recognize
#   - bintype: whether "bins" is a number of bins or a binwidth
#   - title: graph title
#   - titlefontsize: size to set title to
#   - x: x-axis label
#   - y: y-axis label
#   - color: color of bins in histogram
#   - edgecolor: color of bin edges in histogram
#   - edgewidth: linewidth of bin edges in histogram
#   - xmax: upper limit of x-axis
#   - xmin: lower limit of x-axis
#   - ymax: upper limit of y-axis
#   - ymin: lower limit of y-axis
#   - xfontsize: size to set x-axis label to
#   - yfontsize: size to set y-axis label to
#   - width: figure width 
#   - height: figure height
#   - toggle: toggle for whether to show the 0-tick on the y-axis
#   - annotations: list of lines that were added to the figure (from the previous generation)
#   - subtitles: list of subtitles that were added to the figure (from the previous generation)
#   - subtitlesizes: size of subtitles that were added to the figure (from the previous generation)
#   - linecolor: currently selected color for vertical line annotations
#   - linestyle: currently selected style for vertical line annotations
#   - linetogg: whether line edits are currently toggled on
#   - linewidth: line width for vertical line annotations
#   - shift (optional): how much to shift the data by in order to zero the first column
class StackedHistMaker():

    # initializes the variables within the window
    def __init__(self, files, savepath, filename, datacolumn, master, row, col, bins, bintype, 
                 title, titlefontsize, x, y, color, edgecolor, edgewidth, xmax, xmin, ymax, ymin, 
                 xfontsize, yfontsize, width, height, toggle, annotations, subtitles, subtitlesizes,
                 linecolor, linestyle, linetogg, linewidth, shift=None):
        self.files = files
        self.savepath = savepath
        self.filename = filename
        self.datacolumn = datacolumn
        self.master = master
        self.row = row
        self.col = col
        self.bins = bins
        self.bintype = bintype
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
        self.annotations = annotations
        self.subtitles = subtitles
        self.subtitlesizes = subtitlesizes
        self.linecolor = linecolor
        self.linestyle = linestyle
        self.linetogg = linetogg
        self.linewidth = linewidth

        self.fig = self.makeStackedHistogram()

    # generates the stack of histograms based on the parameters set in the customizability window
    def makeStackedHistogram(self):
        self.processData()

        # create a new matplotlib figure
        fig = Figure(dpi=100)
        fig.set_figwidth(self.width)
        fig.set_figheight(self.height)

        # create a new histogram, set parameters
        self.axes = []
        for i in reversed(range(len(self.all_data_shifted))):
            ax = fig.add_subplot(len(self.all_data_shifted), 1, i+1)
            ax.hist(self.all_data_shifted[i][self.datacolumn], bins=self.bins, color=self.color, 
                    edgecolor=self.edgecolor, linewidth=self.edgewidth)
            if len(self.subtitles) != 0:
                ax.annotate(text=self.subtitles[i], fontsize=self.subtitlesizes[i], xy=(0.03, 0.85), xycoords='axes fraction')
            
            else:
                ax.annotate(text=self.lastFolder[i], fontsize=9, xy=(0.03, 0.85), xycoords='axes fraction')
            self.axes.append(ax)

        self.format_axes()
        self.axes[0].set_xlabel(self.x, fontsize=self.xfontsize)
        
        #set title & append figure to canvas
        fig.supylabel(self.y, fontsize=self.yfontsize, x = self.width / 50)
        fig.suptitle(self.title, y = 0.93, x=0.57, fontsize=self.titlesize)
        
        widthpad = 0
        heightpad = 0
        if self.width <= 3.5:
            widthpad = 0.05
            if self.width <= 2.5:
                widthpad = 0.1
        if self.height <= 0.4:
            heightpad = 0.05
            if self.height <=0.3:
                heightpad = 0.1
                if self.height <= 0.25:
                    heightpad = 0.2

        
        fig.subplots_adjust(wspace=0, hspace=0, left=(0.25+widthpad), right=0.9, bottom = (0.2 + heightpad))

        self.hist_canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.hist_canvas.draw()
        self.hist_canvas.get_tk_widget().grid(row=self.row, column=self.col)

        # annotate figure with lines
        fig.canvas.mpl_connect('button_press_event', lambda event: self.onclick(event))
        self.restore_annotations()
        return fig
    
    #set up axis ticks, range, & scale
    def format_axes(self):
        if self.xmin is None:
            self.xmin = self.min_data
        if self.xmax is None:
            self.xmax = self.max_data
            
        for ax in self.axes:
            #ax.sharey(self.axes[0])
            ax.set_xticks([])
            ax.set_xlim([self.xmin, self.xmax])
            ax.set_ylim([self.ymin, self.ymax]) 
            self.xlim = ax.get_xlim()
            self.ylim = ax.get_ylim()
            
            yticks = ax.get_yticklabels()
            if self.toggle == 1:
                yticks[0].set_visible(False)
    
        self.axes[0].xaxis.set_major_locator(plt.AutoLocator())

        # remove x-tick labels on subplots, except for last one
        for i in range(1, len(self.all_data_shifted)):
           self.axes[i].xaxis.set_major_locator(plt.AutoLocator())
           self.axes[i].set_xticklabels([])
    
    # re-add lines from previous generation of histogram
    def restore_annotations(self):
        if len(self.annotations) != 0:
            for annotation in self.annotations:
                axis, x, y, dbl, color, style, lw = annotation
                for ax in self.axes:
                    ax_pos = ax.get_position()
                    axis_pos = axis.get_position()
                    ax0 = ax_pos.y0
                    axis0 = axis_pos.y0
                    if (ax0 == axis0):
                        self.draw_annotations(ax, x, y, color, style, lw)

    # return list of line annotations on histogram
    def get_annotations(self):
        return self.annotations
    
    # return number of plots in stacked histogram
    def get_height(self):
        return len(self.all_data_shifted)
    
    # return list of subtitles on histogram
    def get_subtitles(self):
        return self.subtitles
    
    # return name of last folder in filepath
    def get_lastfolder(self):
        return self.lastFolder
    
    # return list of subtitle sizes on histogram
    def get_subtitlesizes(self):
        return self.subtitlesizes

    # collects data from individual files, compiles them into a list of dataframes
    # and sets the number of bins to use
    def processData(self):
        
        # initialize a list of dataframes
        self.all_data = []
        min_length = float('inf')
        self.min_data = float('inf')
        self.max_data = 0

        # for each file, get the data and the data's bounds
        self.lastFolder = []
        for file in self.files:
            self.lastFolder.append(os.path.basename(file))
            path = os.path.join(file, self.filename)
            data = self.get_eFRET_data(path)

            if len(data) < min_length:
                min_length = len(data)
            if data["eFRET"].min() < self.min_data:
                self.min_data = data["eFRET"].min()
            if data["eFRET"].max() > self.max_data:
                self.max_data = data["eFRET"].max()

            # add data to list
            self.all_data.append(data)
            self.minlength = min_length

        # zero & bin the data
        self.zero_data()
        self.min_data -= float(self.offset)
        self.max_data -= float(self.offset)
        self.setBins()
    
    # sets the number/width of bins to use in the histogram based on input in the customization menu
    # sets the number/width of bins to display in the customization menu
    def setBins(self):
        # if the user didn't enter 'Auto,' check to see if it was a typo
        if self.bins != 'Auto':
            self.autoBinCheck()

        # if the user entered 'Auto,' figure out whether to use auto binning
        # for bin width or bin number
        if self.bins == 'Auto':
            self.makeAutoBins()

        # otherwise, if the user selected to enter a bin width
        # use that value as the bin width
        elif self.bintype == 1:
            self.makeBinWidth()
        
        # otherwise, if the user selected to enter a bin number
        # use the many bins
        else:
            self.bins = int(self.bins)
            self.return_bins = int(self.bins)

    # if we are using a non-auto bin width, create the bins
    def makeBinWidth(self):
        bin_width = float(self.bins)
        rangebin = self.max_data - self.min_data
        numbins = rangebin // bin_width
        bins = np.linspace(self.min_data, self.max_data + bin_width, int(numbins) + 1)
        self.bins = bins 
        self.return_bins = bin_width

    # if the user chose to do auto binning, check to see whether we are using
    # bin width or bin number
    def makeAutoBins(self):
        if self.bintype == 0:
                self.bins = int(self.auto_bin())
                self.return_bins = f'Auto:{self.bins}'
        else:
            bin_width = float(self.auto_bin_width())
            rangebin = self.max_data - self.min_data
            numbins = rangebin // bin_width
            bins = np.linspace(self.min_data, self.max_data + bin_width, int(numbins) + 1)
            self.bins = bins 
            self.return_bins = bin_width

    # check to see if the user meant to type 'Auto' for binning
    def autoBinCheck(self):
        if 'Auto' in str(self.bins):
                self.bins = 'Auto'
        elif 'auto' in str(self.bins):
                self.bins = 'Auto'
        elif float(self.bins) < 1.0:
            if self.bintype == 0:
                self.bins = 'Auto'

    # returns the number of bins used in a histogram
    def getBins(self):
        return self.return_bins

    # returns dataframe from one file
    def get_eFRET_data(self, path):
        FRETresult = open(path, "r") 
        if ".csv" in path:
            data = pd.read_csv(FRETresult, header=None)
        else:
            data = pd.read_fwf(FRETresult, header=None)
        data.columns = ["eFRET", "other"]
        return data

    # zeroes the data in each dataframe generated; can shift by a designated value or do it automatically
    def zero_data(self):
        zeroed_data = []
        for df in self.all_data:
            if self.offset == 'None':
                self.offset = 0.0
            # subtract that value off from all of the eFRET data
            df[self.datacolumn] = df[self.datacolumn].astype(float)
            df[self.datacolumn] = df[self.datacolumn] - float(self.offset)
            zeroed_data.append(df)
        self.all_data_shifted = zeroed_data

    # returns the count of the highest bin, not currently in use
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
    
    # calculates the bin width based on matplotlibs automatic functions
    def auto_bin_width(self):
        hist, bin_edges = np.histogram(self.all_data_shifted[0][self.datacolumn])
        binwidths = bin_edges[1] - bin_edges[0]
        return binwidths

    # saves the figure using matlotlibs savefig functions, based on parameters set in save window
    #   - refpath: filepath to save the file to
    #   - reftype: what kind of file to save as
    #   - refqual: quality of image to save
    def save(self, refpath, reftype, refqual):
        if refqual == "Low":
            dpi=200
        elif refqual == "Medium":
            dpi=400
        elif refqual == "High":
            dpi=600
        refpath += reftype
        self.fig.savefig(refpath, dpi=dpi)
        self.annotate(refpath)

    # removes canvas
    def destroy(self):
        self.hist_canvas.get_tk_widget().destroy()

    # creates .txt file to save parameters, saves at same filepath
    #   - refpath: filepath input in save window; matches figure save filepath
    def annotate(self, refpath):
        # generate annotation text to save
        text = self.getText()

        # generate save path
        refpath2 = refpath.split(".")[:-1]
        pathway = ""
        if len(refpath2) > 0:
            for path in refpath2:
                pathway += path
        else:
            pathway = refpath

        # write and save file
        path = str(pathway) + ".txt"
        f = open(path, "w")
        f.write(text)
        f.close()

    # gathers input parameters and formats it into text to save as a .txt file
    def getText(self):

        # collect information about paramets
        if self.bintype == 1:
            binning = "bin width"
        elif self.bintype == 0:
            binning = "bin number"
        
        xmin, xmax = self.xlim
        ymin, ymax = self.ylim

        if self.toggle == 1:
            togg = "off"
        else:
            togg = "on"

        # format text to insert into .txt file
        text = f"""
        data: {self.datacolumn}
        savepath: {self.savepath}
        bins: {self.bins}
        bintype: {binning}
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
        zero tick: {togg}
        annotations: {self.annotations}
        subtitles: {self.subtitles}
        """
        return text

    # clicking adds vertical line to figure if toggled on
    #   - event: left mouse button press
    def onclick(self, event):
        if self.linetogg == 1:
            if event.inaxes:
                if event.dblclick:
                    self.handleDblClick()
                
                else:
                    axis = (event.inaxes)
                    x, y = event.xdata, event.ydata
                    ymin, ymax = self.ylim

                    dbl=False
                    self.draw_annotations(axis, x, y, self.linecolor, self.linestyle, self.linewidth)
                    self.annotations.append((axis, x, y, dbl, self.linecolor, self.linestyle, self.linewidth))
    
    
    # double clicking adds a vertical line spanning all subplots
    def handleDblClick(self):
        axis, x, y, dbl, color, style, lw = self.annotations[-1]
        for ax in self.axes:
            ax_pos = ax.get_position()
            axis_pos = axis.get_position()
            ax0 = ax_pos.y0
            axis0 = axis_pos.y0
            if (ax0 != axis0):
                dbl=True
                self.draw_annotations(ax, x, y, self.linecolor, self.linestyle, self.linewidth)
                self.annotations.append((ax, x, y, dbl, self.linecolor, self.linestyle, self.linewidth))


    # draws lines on the matplotlib figure, parameters set in customization menu
    #   - axis: where to draw the annotations (on the plot)
    #   - x: x-coordinate (based on the x-axis data) to draw the line at
    #   - y: y-coordinate (unused)
    #   - color: color of the line to paste onto the canvas
    #   - linestyle: style of line to paste onto the canvas
    #   - linewidth: size of line to paste onto the canvas
    def draw_annotations(self, axis, x, y, color, style, lw):
        ymin, ymax = axis.get_ylim()
        annotation = axis.annotate('', xy=(x, 0), xytext=(x, ymax), xycoords='data', 
                                   arrowprops=dict(arrowstyle='-', color=color, 
                                                   linestyle=style, lw=lw))
        arrow_patch = annotation.arrow_patch               
        self.hist_canvas.draw()



