from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import pandas as pd
import tkinter as tk
import os


class FileViewerMaker():

    # title is the full file path
    # title set is the window title aka the parent folder that was inputted
    # data should come in as a dataframe
    def __init__(self, title, titleset, data, master, refcolor1, refcolor2, 
                 refcolor3, graphtitle, graphtitlefontsize, x, xfontsize,
                 x2, x2fontsize, y, yfontsize, y2, y2fontsize, height, width, 
                 xmax, xmin, ymax, ymin, y2max, y2min, intensitytoggle, efficiencytoggle,
                 legendtoggle, subtitletoggle, subtitletoggle2, yshift, clicktogg, sumtogg,
                 dwellActive, dwelltimedf, series):
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
        #self.clicktoggle = 0 #for now
        self.sumtogg = sumtogg
        self.toolbar = None

        self.dwellActive = dwellActive
        self.dwellclick = 1
        self.dwellseries = series
        self.dwelldf = dwelltimedf
     
        self.xmin = 0.0
  
        self.title = title
        self.titleset = titleset
        self.clicked = False
        self.iaxis = None
        self.eaxis = None

        self.datacopy['donor'] = self.data['donor'] - self.yshift
        self.datacopy['acceptor'] = self.data['acceptor'] - self.yshift
        
        self.start()

    def getMinMax(self):
        #print("setting lims")
        return self.xmin, self.xmax, self.ymin, self.ymax, self.y2min, self.y2max

    def getShift(self):
        #print(f"get: {self.yshift}")
        return self.yshift
    
    def setShift(self, yshift):
        self.yshift = yshift

    def start(self):
        self.calculateEfret()
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

        self.fig = Figure()

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

        if self.toolbar != None:
            self.toolbar.destroy()
            self.toolbar = None
            self.master.update_idletasks()

        if self.toolbar == None:
            self.toolbar = NavigationToolbar2Tk(self.trajectorycanvas, self.master, pack_toolbar=False)
            self.toolbar.update()
            self.toolbar.grid(row=1, column=0, sticky="ew")

        self.fig.canvas.mpl_connect('button_press_event', lambda event: self.onclick(event))



    def makeIntensity(self):
        self.iaxis = self.axes[0]
        fig = self.axes[0]
        
        time = self.datacopy["time"]
        donor = self.datacopy["donor"]
        acceptor = self.datacopy["acceptor"]
        self.datacopy["sum"] = self.datacopy["donor"] + self.datacopy["acceptor"]
        summm = self.datacopy["sum"]

        fig.plot(time, donor, color=self.color1, label="Donor", zorder=2)
        fig.plot(time, acceptor, color=self.color2, label="Acceptor", zorder=3)
        if self.sumtogg == 1:
            fig.plot(time, summm, color='black', label="Sum", zorder=1)
        
        if self.legend == 1:
            fig.legend()

        fig.set_xlim([self.xmin, None])
        fig.set_axisbelow(True)
        fig.grid(True, linestyle="--", linewidth=0.8, color='xkcd:light grey')

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

        self.eaxis.sharex(self.iaxis)
        
        time = self.datacopy["time"]
        efret = self.datacopy["efret"]

        fig.plot(time, efret, color=self.color3, zorder=1)
        fig.set_ylim([0, 1]) 
        fig.set_xlim([self.xmin, None])
        
        fig.set_axisbelow(True)
        fig.grid(True, linestyle="--", linewidth=0.8, color='xkcd:light grey')
        
        if self.subtitle2 == 1:
            fig.annotate(text=self.title, xy=(10, 10), xycoords='axes pixels', zorder=2) #toggle on and off

        return fig

    # removes canvas
    def destroyWidget(self):
        self.trajectorycanvas.get_tk_widget().destroy()

    def onclick(self, event):
        if self.clicktoggle == 1:
            if event.inaxes == self.iaxis: # will need to make this specific to each graph
                self.yshift += event.ydata
                self.datacopy['donor'] = self.data['donor'] - self.yshift
                self.datacopy['acceptor'] = self.data['acceptor'] - self.yshift
                self.start()

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

    def calculateEfret(self):
        gamma = 1
        self.datacopy['efret'] = self.datacopy['acceptor'] / (self.datacopy['acceptor'] + (gamma * self.datacopy['donor']))

    def save(self, path, ending):
        path = path.rstrip("\\/")
        self.title = os.path.basename(self.title)
        filename = os.path.join(path, self.title)
        filename = filename + ending

        lowerbound, upperbound  = self.iaxis.get_xlim()
        column_name = 'time' # Replace with the name of your column
        zoomed_df = self.datacopy[(self.datacopy[column_name] >= lowerbound) & (self.datacopy[column_name] <= upperbound)]
        
        zoomed_df_dropped = zoomed_df.drop(columns=["efret", "sum"])
        zoomed_df.to_csv(filename, index=False) # saves zeroed data between x values in a zoomed-in view

    def getDwellData(self):
        return self.dwelldf

    def incrementDwellSeries(self):
        self.dwellseries += 1;
    
    def getDwellSeries(self):
        return self.dwellseries
    
    def saveDwellData(self, filepath, filetype): #filepath = directly entered by user, filetype = .csv
        filename = filepath + filetype
        self.dwelldf.to_csv(filename, index=False)
        print(f"Dwell data saved to {filename}")

    


 