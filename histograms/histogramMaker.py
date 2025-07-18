import numpy as np
import math
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure

#   - data: pandas dataframe column to input into a histogram
#   - savepath: what to set as the default save path
#   - master: which frame of the gui to add the histogram to
#   - row: which row to add canvas to
#   - col: which column to add canvas to
#   - bins: number of bins for histogram to recognize
#   - bin1: whether "bins" is a number of bins or a binwidth
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
#   - annotations: list of lines that were added to the figure (from the previous generation)
#   - linecolor: currently selected color for vertical line annotations
#   - linestyle: currently selected style for vertical line annotations
#   - linetogg: whether line edits are currently toggled on
#   - linewidth: line width for vertical line annotations
#   - shift (optional): how much to shift the data by in order to zero the first column

# creates a histogram to display in the histogramWindow
class HistMaker():

    # initializes variables within the class
    def __init__(self, data, savepath, master, row, col, bins, bin1, title, titlefontsize, 
                 x, y, color, edgecolor, edgewidth, xmax, xmin, ymax, ymin, xfontsize, yfontsize, 
                 width, height, annotations, linecolor, linestyle, linetogg, linewidth, ticktext, shift=None):
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
        self.linecolor = linecolor
        self.linestyle = linestyle
        self.linetogg = linetogg
        self.linewidth = linewidth
        self.ticktext = ticktext
        self.bininput = bins

        # create the figure to be pasted into a HistogramWindow
        self.fig = self.makeHistogram()


    # makes a single histogram from a given data frame column
    def makeHistogram(self):
        
        # copy and modify data according to shift
        self.zero_data()

        # create a new matplotlib figure
        fig = Figure(dpi=100)
        fig.set_figwidth(self.width)
        fig.set_figheight(self.height)
        f = fig.gca()

        # calculate the number of bins to use in the histogram
        self.setBins()


        # create a new histogram, set parameters
        f.hist(self.data_shifted, bins=self.bins, color=self.color, edgecolor=self.edgecolor, linewidth=self.edgewidth)
        
        # set axes options
        f.set_xlabel(self.x, fontsize=self.xfontsize)
        f.set_ylabel(self.y, fontsize=self.yfontsize)
        f.set_xlim([self.xmin, self.xmax])
        f.set_ylim([self.ymin, self.ymax])

        self.processTicks(f)
        f.set_yticks(self.ticktext)
        self.xlim = f.get_xlim()
        self.ylim = f.get_ylim()

        #set title & append figure to canvas
        f.set_title(self.title, fontsize=self.titlesize)
        fig.tight_layout()
        self.hist_canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.hist_canvas.draw()
        self.hist_canvas.get_tk_widget().grid(row=self.row, column=self.col)

        # annotate figure with lines, carry over previous annotations
        fig.canvas.mpl_connect('button_press_event', lambda event: self.onclick(event))
        self.restoreAnnotations(f)

        return fig
    
    def processTicks(self, f):
        if self.ticktext == "":
            self.ticktext = f.get_yticks()
        else:
            self.ticktext = self.ticktext.strip(",")
            self.ticktext = self.ticktext.strip()
            self.ticktext = self.ticktext.strip(",")
            self.ticktext = self.ticktext.split(",")
            temp = []
            for val in self.ticktext:
                val = val.strip()
                val = float(val)
                val = round(val, 1)
                temp.append(val)
            self.ticktext = temp
    
    def getTicks(self):
        return self.ticktext
    
    # re-add lines from previous generation of histogram
    #   - f: figure to add the annotations to
    def restoreAnnotations(self, f):
        if len(self.annotations) != 0:
            for annotation in self.annotations:
                x, color, style, lw = annotation
                self.draw_annotations(f, x, color, style, lw)
    

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
    
    # check to see if the user meant to type 'Auto' for binning
    def autoBinCheck(self):
        if 'Auto' in str(self.bins):
                self.bins = 'Auto'
        elif 'auto' in str(self.bins):
                self.bins = 'Auto'
        elif float(self.bins) < 1.0:
            if self.bintype == 0:
                self.bins = 'Auto'

    # if the user chose to do auto binning, check to see whether we are using
    # bin width or bin number
    def makeAutoBins(self):
        if self.bintype == 0:
                self.bins = int(self.auto_bin())
                self.return_bins = f'Auto:{self.bins}'
        else:
            bin_width = float(self.auto_bin_width())
            rangebin = max(self.data_shifted) - min(self.data_shifted)
            numbins = rangebin // bin_width
            bins = np.linspace(min(self.data_shifted), max(self.data_shifted) + bin_width, int(numbins) + 1)
            self.bins = bins 
            self.return_bins = bin_width

    # if we are using a non-auto bin width, create the bins
    def makeBinWidth(self):
        bin_width = float(self.bins)
        rangebin = max(self.data_shifted) - min(self.data_shifted)
        numbins = rangebin // bin_width
        bins = np.linspace(min(self.data_shifted), max(self.data_shifted) + bin_width, int(numbins) + 1)
        self.bins = bins 
        self.return_bins = bin_width

    #returns number of bins used in the histogram
    def getBins(self):
        return self.return_bins
    
    # return list of line annotations on histogram
    def getAnnotations(self):
        return self.annotations

    # zeroes the data in the dataframe; can shift by a designated value or do it automatically
    # authored by Kate Sanders
    def zero_data(self):

        # Make a histogram with two bins, so one bin in actual fret and the other is photobleaching
        if self.offset == 'Auto':
            bin_edges = np.histogram(self.data, bins=2)[1]
            self.offset = bin_edges[1] / 2 # divide the far edge of the first bin (photobleached) by 2 to get the midpoint

        elif self.offset == 'None':
            self.offset = 0.0

        # subtract that midpoint of from all of the eFRET data
        self.data = self.data.astype(float)
        self.data_shifted = self.data - float(self.offset)

    # calculates the number of bins based on size of dataset, using Sturges's Rule (log2n + 1) * 5
    def auto_bin(self):
        n = self.data.count()
        logn = math.ceil(math.log2(n))
        return str(5*(logn + 1))

    # calculates the bin width based on matplotlibs automatic functions
    def auto_bin_width(self):
        hist, bin_edges = np.histogram(self.data_shifted)
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
        # if bintype = 1, bin width; otherwise bin number
        if self.bintype == 1:
            binning = "bin width"
        elif self.bintype == 0:
            binning = "bin number"
        
        # get the axes limits
        xmin, xmax = self.xlim
        ymin, ymax = self.ylim
        

        # format text to insert into .txt file
        text = f"""
        data: {self.data}
        savepath: {self.savepath}
        bins: {self.bins} 
        bintype: {binning} ({self.bininput})
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
        y-ticks: {self.ticktext}
        x-axis label fontsize: {self.xfontsize}
        y-axis label fontsize: {self.yfontsize}
        offset: {self.offset}
        figure width: {self.width}
        figure height: {self.height} 
        annotations: {self.annotations}
        linecolor: {self.linecolor}
        linestyle: {self.linestyle}
        linetogg: {self.linetogg}
        linewidth: {self.linewidth}

        """
        return text
    
    # clicking adds vertical line to figure if toggled on
    #   - event: left mouse button press
    def onclick(self, event):
        if self.linetogg == 1:
            if event.inaxes:
                x = event.xdata
                self.draw_annotations(event.inaxes, x, self.linecolor, self.linestyle, self.linewidth)
                print(f"x-value: {x}")
                self.annotations.append((x, self.linecolor, self.linestyle, self.linewidth))
    
    # draws lines on the matplotlib figure, parameters set in customization menu
    #   - axis: where to draw the annotations (on the plot)
    #   - x: x-coordinate (based on the x-axis data) to draw the line at
    #   - color: color of the line to paste onto the canvas
    #   - linestyle: style of line to paste onto the canvas
    #   - linewidth: size of line to paste onto the canvas
    def draw_annotations(self, axis, x, color, linestyle, linewidth):
        canvas = self.hist_canvas
        ymin, ymax = self.ylim
        axis.annotate('', xy=(x, 0), xytext=(x, ymax), xycoords='data', 
                      arrowprops=dict(arrowstyle='-', color=color, 
                                      linestyle=linestyle, linewidth=linewidth))
        canvas.draw()
        
        




