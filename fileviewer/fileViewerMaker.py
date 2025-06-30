from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import pandas as pd
import tkinter as tk
import os

GAMMA = 1.0

# creates the graph which is pasted into the fileViewerWindow
# must be regenerated after changes are made in the window
#   - title: molecule number
#   - titleset: window title, parent folder input by the user
#   - data: dataframe containing input data
#   - master: frame to paste the graph into
#   - refcolor1: color of donor fluorophore graph line
#   - refcolor2: color of acceptor fluorophore graph line
#   - refcolor3: color of FRET efficiency graph line
#   - graphtitle: title displayed on graph, should match the window title
#   - graphtitlefontsize: size of graphtitle
#   - x: x-axis label for fluorophore intensity graph
#   - xfontsize: size of x
#   - x2: x-axis label for FRET efficiency intensity graph
#   - x2fontsize: size of x2
#   - y: label for y-axis of fluorophore intensity graph
#   - yfontsize: size of y
#   - y2: label for y-axis of FRET efficiency intensity graph
#   - y2fontsize: size of y2
#   - height: height of figure
#   - width: width of figure
#   - intensitytoggle: fluorophore intensity graph toggle, default = ON
#   - efficiencytoggle: FRET efficiency graph toggle, default = ON
#   - legendtoggle: fluorophore intensity graph legend (donor vs acceptor color) toggle, default = OFF
#   - subtitletoggle: fluorophore intensity subtitle graph toggle, default = ON
#   - subtitletoggle2: FRET efficiency subtitle graph toggle, default = ON
#   - yshift: how much to subtract from the data when zeroing, carries over between generations but not separate trajectories
#   - clicktogg: designates whether the click-to-zero function is active, default = OFF
#   - sumtogg: designates whether the sum of fluorophore intensities is shown on the fluorophore intensity graph, default = OFF
#   - dwellActive: designates whether the click-to-select dwell times is active, default = OFF
#   - dwelltimedf: stores the dwell time data, carries over between generations but not separate trajectories (IS THIS TRUE?)
#   - series: tracks what value the series variable is at between generations
#   - tracenum: hel number, used for saving the molecule
#   - molnum: molecule number

class FileViewerMaker():

    # initialize variables within the class
    def __init__(self, title, titleset, data, master, refcolor1, refcolor2, 
                 refcolor3, graphtitle, graphtitlefontsize, x, xfontsize,
                 x2, x2fontsize, y, yfontsize, y2, y2fontsize, height, width, 
                 intensitytoggle, efficiencytoggle, legendtoggle, subtitletoggle, 
                 subtitletoggle2, yshift, clicktogg, sumtogg,
                 dwellActive, dwelltimedf, series, tracenum, molnum):
        # designate data
        self.data = data
        self.datacopy = data.copy() # copy data to new dataframe, so it can be modified without loss
        self.master = master
        self.tracenum = tracenum[0]
        self.molnum = molnum
        
        # set colors for graph
        self.color1 = refcolor1
        self.color2 = refcolor2
        self.color3 = refcolor3

        # set text & text sizes for graph
        self.graphtitle = graphtitle
        self.titlefontsize = graphtitlefontsize
        self.xlabel = x
        self.xfontsize = xfontsize
        self.x2label = x2
        self.x2fontsize = x2fontsize
        self.ylabel = y
        self.yfontsize = yfontsize
        self.y2label = y2
        self.y2fontsize = y2fontsize
        self.title = title
        self.titleset = titleset

        # set figure dimensions
        self.width = width
        self.height = height

        # set toggles
        self.intensitytoggle = intensitytoggle
        self.efficiencytoggle = efficiencytoggle
        self.legend = legendtoggle
        self.subtitle = subtitletoggle
        self.subtitle2 = subtitletoggle2
        self.clicktoggle = clicktogg
        self.sumtogg = sumtogg

        # set yshift
        self.yshift = yshift
        self.toolbar = None

        # set dwell time data
        self.dwellActive = dwellActive
        self.dwellclick = 1
        self.dwellseries = series
        self.dwelldf = dwelltimedf
        self.clicked = False
     
        # set other variables
        self.xmin = 0.0
        self.iaxis = None
        self.eaxis = None

        # generate zeroed data
        self.datacopy['donor'] = self.data['donor'] - self.yshift
        self.datacopy['acceptor'] = self.data['acceptor'] - self.yshift
        
        self.start()

    # return x and y limit for both the fluorophore intensity and FRET efficiency graphs
    def getMinMax(self):
        return self.xmin, self.xmax, self.ymin, self.ymax, self.y2min, self.y2max

    # return y shift
    def getShift(self):
        return self.yshift
    
    # set y shift
    def setShift(self, yshift):
        self.yshift = yshift

    # generate graphs to add to figure
    def start(self):
        # generate FRET efficiency values from fluorophore intensities
        self.calculateEfret()
        # get the title from the input keys
        self.makeTitle()
        # generate the fluorophore intensity and FRET efficiency subplots
        self.makeSubplots()

        # configure the figure containing the subplots onto the window
        self.trajectorycanvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.trajectorycanvas.draw()
        self.trajectorycanvas.get_tk_widget().grid(row=0, column=0)
        self.setToolbar()

        # connect clicks to zeroing & dwell time activities
        self.fig.canvas.mpl_connect('button_press_event', lambda event: self.onclick(event))

    # get figure subtitle from keys
    def makeTitle(self):
        keys = self.title.split("/")
        self.title = ""
        count = False
        for i in range(len(keys)):
            if count:
                self.title += "/" + keys[i]
            if keys[i] == self.titleset:
                count = True
        self.title = self.title.split(".")[0]
        self.title = self.title.strip("/")
    
    # generate and arrange the two subfigures
    def makeSubplots(self):
        self.fig = Figure()
        axesnum = self.efficiencytoggle + self.intensitytoggle
        self.axes = []
        for i in range(axesnum):
            ax = self.fig.add_subplot(axesnum, 1, i+1)
            self.axes.append(ax)

        # generate the subplots
        if self.intensitytoggle == 1:
            self.makeIntensity()
        if self.efficiencytoggle == 1:
            self.makeEfficiency()

        self.fig.subplots_adjust(wspace=0, hspace=0.5, left=0.1, right=0.9)
        self.fig.suptitle(self.graphtitle, fontsize=self.titlefontsize, y=0.93)

    # add a toolbar to the window, connected to the subfigures
    def setToolbar(self):
        if self.toolbar != None:
            self.toolbar.destroy()
            self.toolbar = None
            self.master.update_idletasks()

        if self.toolbar == None:
            self.toolbar = NavigationToolbar2Tk(self.trajectorycanvas, self.master, pack_toolbar=False)
            self.toolbar.update()
            self.toolbar.grid(row=1, column=0, sticky="ew")
    
    # generate fluorophore intensity graph
    def makeIntensity(self):

        # the first graph should be the intensity graph
        self.iaxis = self.axes[0]
        fig = self.axes[0]
        
        # set up & plot the data columns on the figure
        time = self.datacopy["time"]
        donor = self.datacopy["donor"]
        acceptor = self.datacopy["acceptor"]
        self.datacopy["sum"] = self.datacopy["donor"] + self.datacopy["acceptor"]
        summm = self.datacopy["sum"]
        fig.plot(time, donor, color=self.color1, label="Donor", zorder=2)
        fig.plot(time, acceptor, color=self.color2, label="Acceptor", zorder=3)
        
        # set axis options
        fig.set_xlim([self.xmin, None])
        fig.set_xlabel(self.xlabel, fontsize=self.xfontsize)
        fig.set_ylabel(self.ylabel, fontsize=self.yfontsize)
        fig.set_axisbelow(True)
        fig.grid(True, linestyle="--", linewidth=0.8, color='xkcd:light grey')

        # toggle options: show sum, show the legend, or show the subtitle
        if self.sumtogg == 1:
            fig.plot(time, summm, color='black', label="Sum", zorder=1)
        if self.legend == 1:
            fig.legend()
        if self.subtitle == 1:
            fig.annotate(text=self.title, xy=(10, 10), xycoords='axes pixels', zorder=3)
        
        return fig
        
    # generate FRET efficiency graph
    def makeEfficiency(self):
        
        # the second graph should be the efficiency, unless the intensity graph is toggled off
        if self.intensitytoggle == 1:
            fig = self.axes[1]
            self.eaxis = self.axes[1]
        elif self.intensitytoggle == 0:
            fig = self.axes[0]
            self.eaxis = self.axes[0]

        # set up & plot the data columns on the figure
        self.eaxis.sharex(self.iaxis) 
        time = self.datacopy["time"]
        efret = self.datacopy["efret"]
        fig.plot(time, efret, color=self.color3, zorder=1)
        
        # set axis options
        fig.set_ylim([0, 1]) 
        fig.set_xlim([self.xmin, None])
        fig.set_xlabel(self.x2label, fontsize=self.x2fontsize)
        fig.set_ylabel(self.y2label, fontsize=self.y2fontsize)
        fig.set_axisbelow(True)
        fig.grid(True, linestyle="--", linewidth=0.8, color='xkcd:light grey')
        
        # toggle option: show the subtitle
        if self.subtitle2 == 1:
            fig.annotate(text=self.title, xy=(10, 10), xycoords='axes pixels', zorder=2) #toggle on and off

        return fig

    # removes canvas 
    def destroyWidget(self):
        self.trajectorycanvas.get_tk_widget().destroy()

    # handles all click events
    def onclick(self, event):

        # if the click-to-zero is active, zeroes data to y-value of click
        if self.clicktoggle == 1:
            if event.inaxes == self.iaxis: # will need to make this specific to each graph
                self.yshift += event.ydata
                self.datacopy['donor'] = self.data['donor'] - self.yshift
                self.datacopy['acceptor'] = self.data['acceptor'] - self.yshift
                self.start()

        # if the click-to-select dwell times is active, tracks first and second clicks
        # records the difference between the clicks in a dataframe
        elif self.dwellActive:
            if event.inaxes == self.iaxis:
                if self.dwellclick == 1:
                    self.first_click = event.xdata
                    self.dwellclick += 1
                elif self.dwellclick == 2:
                    self.second_click = event.xdata
                    self.dwellclick = 1
                    deltaT = abs(self.first_click - self.second_click)
                    self.dwelldf.loc[len(self.dwelldf)] = [self.dwellseries, deltaT]

    # calculates the FRET efficiency for each row in the provided trajectory data
    # GAMMA can be altered to suit the needs of the user
    def calculateEfret(self):
        gamma = GAMMA
        self.datacopy['efret'] = self.datacopy['acceptor'] / (self.datacopy['acceptor'] + (gamma * self.datacopy['donor']))

    # saves the data as a csv, including the time, donor, and acceptor columns
    #   - path: file path to which to save the data
    #   - ending: filetype to save the data as, default .csv
    def save(self, path, ending):
        path = path.rstrip("\\/")
        # make exact name of file
        self.title = str(self.tracenum) + " tr" + str(self.molnum)
        filename = os.path.join(path, self.title)
        filename = filename + ending

        # saves zeroed data between x values in a zoomed-in view
        lowerbound, upperbound  = self.iaxis.get_xlim()
        column_name = 'time'
        zoomed_df = self.datacopy[(self.datacopy[column_name] >= lowerbound) & (self.datacopy[column_name] <= upperbound)]
        zoomed_df_dropped = zoomed_df.drop(columns=["efret", "sum"])
        if ending == ".csv":
            zoomed_df_dropped.to_csv(filename, index=False) 
        else:
            col_widths = [20, 20, 20]
            self.write_fwf(zoomed_df_dropped, filename, col_widths)

    # returns dataframe containing dwell time data
    def getDwellData(self):
        return self.dwelldf

    # increments series value for dwell time analysis by one
    def incrementDwellSeries(self):
        self.dwellseries += 1;
    
    # returns the series value for dwell time analysis
    def getDwellSeries(self):
        return self.dwellseries
    
    # saves the dwell time analysis data as a dataframe
    #   - filepath: filepath to which to save the dataframe, directly entered by the user
    #   - filetype: filetype to save the data as, default .csv
    def saveDwellData(self, filepath, filetype): #filepath = directly entered by user, filetype = .csv
        filename = filepath + filetype
        self.dwelldf.to_csv(filename, index=False)


    # export data to a fwf (dat) file, using white space as the delimiter
    def write_fwf(self, df, filepath, col_widths, justify='left'):
        with open(filepath, 'w') as f:
            for _, row in df.iterrows():
                formatted_row = ''
                for i, value in enumerate(row):
                    format_string = '{:<' + str(col_widths[i]) + '}' if justify == 'left' else '{:>' + str(col_widths[i]) + '}'
                    formatted_row += format_string.format(str(value))
                f.write(formatted_row + '\n')