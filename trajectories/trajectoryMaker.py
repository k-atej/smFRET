from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
import pandas
import os

GAMMA = 1.0

# creates the graph which is pasted into the trajectoryWindow
# must be regenerated after changes are made in the window
#   - title: full file path
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
#   - xmax: max x-axis value
#   - xmin: min x-axis value
#   - ymax: max y-axis value, intensity figure
#   - ymin: min y-axis value, intensity figure
#   - y2max: max y-axis value, FRET efficiency figure
#   - y2min: min y-axis value, FRET efficiency figure
#   - intensitytoggle: fluorophore intensity graph toggle, default = ON
#   - efficiencytoggle: FRET efficiency graph toggle, default = ON
#   - legendtoggle: fluorophore intensity graph legend (donor vs acceptor color) toggle, default = OFF
#   - subtitletoggle: fluorophore intensity subtitle graph toggle, default = ON
#   - subtitletoggle2: FRET efficiency subtitle graph toggle, default = ON
#   - yshift: how much to subtract from the data when zeroing, carries over between generations but not separate trajectories
#   - clicktogg: designates whether the click-to-zero function is active, default = OFF
#   - linesize1, 2, & 3: linewidths for each plot
class TrajectoryMaker():

    # initializes variables within the class
    def __init__(self, title, titleset, data, master, refcolor1, refcolor2, 
                 refcolor3, graphtitle, graphtitlefontsize, x, xfontsize,
                 x2, x2fontsize, y, yfontsize, y2, y2fontsize, height, width, 
                 xmax, xmin, ymax, ymin, y2max, y2min, intensitytoggle, efficiencytoggle,
                 legendtoggle, subtitletoggle, subtitletoggle2, yshift, eyshift, clicktogg,
                 linesize1, linesize2, linesize3, iticks, eticks):
        #designate data
        self.data = data
        self.datacopy = data.copy()
        self.master = master

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
        self.clicked = False

        # set yshift
        self.yshift = yshift
        self.eyshift = eyshift

        # set axis variables
        self.xmax = xmax
        self.xmin = xmin
        self.ymax = ymax
        self.ymin = ymin
        self.yticks = iticks
        self.y2max = y2max
        self.y2min = y2min
        self.y2ticks = eticks
        if self.y2ticks == "":
            self.y2ticks = [0.0, 0.5, 1.0]
            temp = []
            for val in self.y2ticks:
                val = float(val)
                val = round(val, 1)
                temp.append(val)
            self.y2ticks = temp

        self.iaxis = None
        self.eaxis = None

        # set linewidths
        self.linewidth1 = linesize1
        self.linewidth2 = linesize2
        self.linewidth3 = linesize3

        # generate zeroed data
        self.datacopy['donor'] = self.data['donor'] - self.yshift
        self.datacopy['acceptor'] = self.data['acceptor'] - self.yshift
        self.datacopy['efret'] = self.data['efret'] - self.eyshift
        
        self.start()

    # return x and y limit for both the fluorophore intensity and FRET efficiency graphs
    def getMinMax(self):
        return self.xmin, self.xmax, self.ymin, self.ymax, self.y2min, self.y2max, self.yticks, self.y2ticks

    # return y shift
    def getShift(self):
        return self.yshift, self.eyshift
    
    # set y shift
    def setShift(self, yshift, eyshift):
        self.yshift = yshift
        self.eyshift = eyshift


    # generate graphs and add to figure
    def start(self):
        # get the title from the input keys
        self.makeTitle()
        # configure size of figure
        self.fig = Figure(constrained_layout=True)
        self.fig.set_figwidth(self.width)
        self.fig.set_figheight(self.height)

        # generate the fluorophore intensity and FRET efficiency subplots
        self.makeSubplots()

        # configure the canvas containing the subplots
        #self.fig.subplots_adjust(wspace=0, hspace=0.5, left=0.1, right=0.9)
        self.fig.suptitle(self.graphtitle, fontsize=self.titlefontsize) #y=0.93
        self.trajectorycanvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.trajectorycanvas.draw()
        self.trajectorycanvas.get_tk_widget().grid(row=0, column=0)

        # connect clicks to zeroing
        self.fig.canvas.mpl_connect('button_press_event', lambda event: self.onclick(event))

    # generate the fluorophore intensity and FRET efficiency subplots
    def makeSubplots(self):
        axesnum = self.efficiencytoggle + self.intensitytoggle
        self.axes = []
        for i in range(axesnum):
            ax = self.fig.add_subplot(axesnum, 1, i+1)
            self.axes.append(ax)

        if self.intensitytoggle == 1:
            self.makeIntensity()
        if self.efficiencytoggle == 1:
            self.makeEfficiency()
    
    # get figure subtitle from keys
    def makeTitle(self):
        self.title = self.title.rstrip("\\/")
        keys = self.title.split(os.sep)
        self.title = ""

        count = False
        for i in range(len(keys)): #for each part of the file path
            if count:
                self.title += "/" + keys[i]
            if keys[i] == self.titleset:
                count = True

        self.title = self.title.split(".")[0] #removes file type designation
        self.title = self.title.strip("\\/") #removes trailing/leading slashes

    # generate fluorophore intensity graph
    def makeIntensity(self):

        # the first graph should be the intensity graph
        self.iaxis = self.axes[0]
        fig = self.axes[0]
        
        # set up & plot the data columns on the figure
        time = self.datacopy["time"]
        donor = self.datacopy["donor"]
        acceptor = self.datacopy["acceptor"]
        fig.plot(time, donor, color=self.color1, label="Donor", zorder=1, linewidth=self.linewidth1)
        fig.plot(time, acceptor, color=self.color2, label="Acceptor", zorder=2, linewidth=self.linewidth2)

        if self.yticks == "":
            self.yticks = fig.get_yticks()
            temp = []
            for val in self.yticks:
                val = float(val)
                val = round(val, 1)
                temp.append(val)
            self.yticks = temp
    
        # set axis options
        fig.set_xlabel(self.xlabel, fontsize=self.xfontsize)
        fig.set_ylabel(self.ylabel, fontsize=self.yfontsize)
        fig.set_yticks(self.yticks)
        fig.set_xlim([self.xmin, self.xmax])
        fig.set_ylim([self.ymin, self.ymax])

        self.xmin, self.xmax = fig.get_xlim()
        self.ymin, self.ymax = fig.get_ylim()

        # toggle options
        if self.legend == 1:
            fig.legend()
        if self.subtitle == 1:
            fig.annotate(text=self.title, xy=(10, 10), xycoords='axes pixels', zorder=3)
        
        return fig
        
    # generate FRET efficiency graph
    def makeEfficiency(self):

        # the second graph should be the efficiency, 
        # unless the intensity graph is toggled off
        if self.intensitytoggle == 1:
            fig = self.axes[1]
            self.eaxis = self.axes[1]
        elif self.intensitytoggle == 0:
            fig = self.axes[0]
            self.eaxis = self.axes[0]
        
        # set up & plot the data columns on the figure
        time = self.datacopy["time"]
        efret = self.datacopy["efret"]
        fig.plot(time, efret, color=self.color3, zorder=1, linewidth=self.linewidth3)

        # set axis options
        fig.set_ylim([0, 1]) 
        fig.set_ylabel(self.y2label, fontsize=self.y2fontsize)
        fig.set_xlabel(self.x2label, fontsize=self.x2fontsize)
        fig.set_xlim([self.xmin, self.xmax])
        fig.set_yticks(self.y2ticks)
        fig.set_ylim([self.y2min, self.y2max])

        self.y2min, self.y2max = fig.get_ylim()

        # toggle options
        if self.subtitle2 == 1:
            fig.annotate(text=self.title, xy=(10, 10), xycoords='axes pixels', zorder=2) #toggle on and off

        return fig
    
    # saves the graph
    #   - refpath: file path to which to save the image
    #   - reftype: filetype to save the image as
    #   - refqual: quality to save the image
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
        self.trajectorycanvas.get_tk_widget().destroy()

    # handles all click events
    def onclick(self, event):
        if self.clicktoggle == 1:
            if event.inaxes == self.iaxis: # will need to make this specific to each graph
                self.yshift += event.ydata
                self.datacopy['donor'] = self.data['donor'] - self.yshift
                self.datacopy['acceptor'] = self.data['acceptor'] - self.yshift
                self.start()
            elif event.inaxes == self.eaxis: # will need to make this specific to each graph
                self.eyshift += event.ydata
                self.datacopy['efret'] = self.data['efret'] - self.eyshift
                self.start()

    # calculate FRET efficiency, not currenly in use
    def calculateEfret(self):
        gamma = GAMMA
        self.datacopy['efret'] = self.datacopy['acceptor'] / (self.datacopy['acceptor'] + (gamma * self.datacopy['donor']))

    # creates .txt file to save parameters, saves at same filepath
    #   - refpath: filepath input in save window; matches figure save filepath
    def annotate(self, refpath):
        text = self.getText()
        refpath = refpath.split(".")[:-1]
        pathway = ""
        for path in refpath:
            pathway += path
        path = str(pathway) + ".txt"
        f = open(path, "w")
        f.write(text)
        f.close()

    # gathers input parameters and formats it into text to save as a .txt file
    def getText(self):
    
        # format text to insert into .txt file
        text = f"""
        data: {self.data}
        path: {self.title}
        title: {self.graphtitle}
        title fontsize: {self.titlefontsize}
        x-axis label: {self.xlabel}
        y-axis label: {self.ylabel}
        x-axis label fontsize: {self.xfontsize}
        y-axis label fontsize: {self.yfontsize}
        x-axis label: {self.x2label}
        y-axis label: {self.y2label}
        x-axis label fontsize: {self.x2fontsize}
        y-axis label fontsize: {self.y2fontsize}
        color 1: {self.color1}
        color 2: {self.color2}
        color 3: {self.color3}
        x-axis max: {self.xmax}
        x-axis min: {self.xmin}
        y-axis max: {self.ymax}
        y-axis min: {self.ymin}
        y-axis 2 max: {self.y2max}
        y-axis 2 min: {self.y2min}
        
        offset: {self.yshift, self.eyshift}
        legend: {self.legend}
        figure width: {self.width}
        figure height: {self.height} 

        intensity plot: {self.intensitytoggle}
        efficiency plot: {self.efficiencytoggle}
        intensity plot subtitle:{self.subtitle}
        efficiency plot subtitle: {self.subtitle2}

        """
        return text
    
 