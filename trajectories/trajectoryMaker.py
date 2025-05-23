from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
import pandas
import os


class TrajectoryMaker():

    # title is the full file path
    # title set is the window title aka the parent folder that was inputted
    # data should come in as a dataframe
    def __init__(self, title, titleset, data, master, refcolor1, refcolor2, 
                 refcolor3, graphtitle, graphtitlefontsize, x, xfontsize,
                 x2, x2fontsize, y, yfontsize, y2, y2fontsize, height, width, 
                 xmax, xmin, ymax, ymin, y2max, y2min, intensitytoggle, efficiencytoggle,
                 legendtoggle, subtitletoggle, subtitletoggle2, yshift, clicktogg):
        self.data = data
        self.datacopy = data.copy()
        self.master = master
        self.color1 = refcolor1
        self.color2 = refcolor2
        self.color3 = refcolor3
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
        self.width = width
        self.height = height
        self.intensitytoggle = intensitytoggle
        self.efficiencytoggle = efficiencytoggle
        self.legend = legendtoggle
        self.subtitle = subtitletoggle
        self.subtitle2 = subtitletoggle2
        self.yshift = yshift
        self.clicktoggle = clicktogg

        self.xmax = xmax
        self.xmin = xmin
        self.ymax = ymax
        self.ymin = ymin
        self.y2max = y2max
        self.y2min = y2min
        self.title = title
        self.titleset = titleset
        self.clicked = False
        self.iaxis = None
        self.eaxis = None

        self.datacopy['donor'] = self.data['donor'] - self.yshift
        self.datacopy['acceptor'] = self.data['acceptor'] - self.yshift
        
        self.start()

    def getMinMax(self):
        return self.xmin, self.xmax, self.ymin, self.ymax, self.y2min, self.y2max

    def getShift(self):
        return self.yshift
    
    def setShift(self, yshift):
        self.yshift = yshift

    def start(self):
        self.calculateEfret()
        self.makeTitle()
        self.fig = Figure()

        self.fig.set_figwidth(self.width)
        self.fig.set_figheight(self.height)

        axesnum = self.efficiencytoggle + self.intensitytoggle
        self.axes = []
        for i in range(axesnum):
            ax = self.fig.add_subplot(axesnum, 1, i+1)
            self.axes.append(ax)

        if self.intensitytoggle == 1:
            self.makeIntensity()
        if self.efficiencytoggle == 1:
            self.makeEfficiency()

        self.fig.subplots_adjust(wspace=0, hspace=0.5, left=0.1, right=0.9)
        self.fig.suptitle(self.graphtitle, fontsize=self.titlefontsize, y=0.93)

        self.trajectorycanvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.trajectorycanvas.draw()
        self.trajectorycanvas.get_tk_widget().grid(row=0, column=0)

        self.fig.canvas.mpl_connect('button_press_event', lambda event: self.onclick(event))

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



    def makeIntensity(self):
        self.iaxis = self.axes[0]
        fig = self.axes[0]
        
        time = self.datacopy["time"]
        donor = self.datacopy["donor"]
        acceptor = self.datacopy["acceptor"]

        fig.plot(time, donor, color=self.color1, label="Donor", zorder=1)
        fig.plot(time, acceptor, color=self.color2, label="Acceptor", zorder=2)
        
        if self.legend == 1:
            fig.legend()
        fig.set_xlabel(self.xlabel, fontsize=self.xfontsize)
        fig.set_ylabel(self.ylabel, fontsize=self.yfontsize)
        fig.set_xlim([self.xmin, self.xmax])
        fig.set_ylim([self.ymin, self.ymax])

        self.xmin, self.xmax = fig.get_xlim()
        self.ymin, self.ymax = fig.get_ylim()

        if self.subtitle == 1:
            fig.annotate(text=self.title, xy=(10, 10), xycoords='axes pixels', zorder=3)
        
        return fig
        
    
    def makeEfficiency(self):
        if self.intensitytoggle == 1:
            fig = self.axes[1]
            self.eaxis = self.axes[1]
        elif self.intensitytoggle == 0:
            fig = self.axes[0]
            self.eaxis = self.axes[0]
        
        time = self.datacopy["time"]
        efret = self.datacopy["efret"]

        fig.plot(time, efret, color=self.color3, zorder=1)
        fig.set_ylim([0, 1]) 
        fig.set_ylabel(self.y2label, fontsize=self.y2fontsize)
        fig.set_xlabel(self.x2label, fontsize=self.x2fontsize)
        fig.set_xlim([self.xmin, self.xmax])
        fig.set_ylim([self.y2min, self.y2max])

        self.y2min, self.y2max = fig.get_ylim()

        if self.subtitle2 == 1:
            fig.annotate(text=self.title, xy=(10, 10), xycoords='axes pixels', zorder=2) #toggle on and off

        return fig
    
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
        print("SAVED!")

    # removes canvas
    def destroy(self):
        self.trajectorycanvas.get_tk_widget().destroy()

    def onclick(self, event):
        if self.clicktoggle == 1:
            if event.inaxes == self.iaxis: # will need to make this specific to each graph
                self.yshift += event.ydata
                self.datacopy['donor'] = self.data['donor'] - self.yshift
                self.datacopy['acceptor'] = self.data['acceptor'] - self.yshift
                self.start()

    def calculateEfret(self):
        gamma = 1
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
        
        offset: {self.yshift}
        legend: {self.legend}
        figure width: {self.width}
        figure height: {self.height} 

        intensity plot: {self.intensitytoggle}
        efficiency plot: {self.efficiencytoggle}
        intensity plot subtitle:{self.subtitle}
        efficiency plot subtitle: {self.subtitle2}

        """
        return text
    
 