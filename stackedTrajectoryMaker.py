from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
from matplotlib import pyplot as plt


class StackedTrajectoryMaker():

    # title is the full file path
    # title set is the window title aka the parent folder that was inputted
    # data should come in as a dataframe
    def __init__(self, all_data, master, title, refcolor1, refcolor2, refcolor3, 
                 graphtitle, graphtitlesize, x, xfontsize, x2, x2fontsize, y, yfontsize, y2, y2fontsize, 
                 height, width, xmax, xmin, ymax, ymin, y2max, y2min):
        self.all_data = all_data
        self.master = master
        self.title = title
        self.color1 = refcolor1
        self.color2 = refcolor2
        self.color3 = refcolor3
        self.xlabel = x
        self.xfontsize = xfontsize
        self.x2label = x2
        self.x2fontsize = x2fontsize
        self.ylabel = y
        self.yfontsize = yfontsize
        self.y2label = y2
        self.y2fontsize = y2fontsize
        self.title = graphtitle
        self.titlefontsize = graphtitlesize

        self.xmax = xmax
        self.xmin = xmin
        self.ymax = ymax
        self.ymin = ymin
        self.y2max = y2max
        self.y2min = y2min

        self.fig = Figure()
        self.fig.set_figwidth(width)
        self.fig.set_figheight(height)
            
        self.processData()
        if self.xmax == None:
            self.xmax = self.maxtime
        self.makeIntensity()
        self.makeEfficiency()

        self.fig.subplots_adjust(wspace=0.4, hspace=0, left=0.2, right=0.9)
        self.fig.suptitle(self.title, y = 0.93, x=0.55, fontsize=self.titlefontsize)

        self.trajectorycanvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.trajectorycanvas.draw()
        self.trajectorycanvas.get_tk_widget().grid(row=0, column=0, padx=(5, 5))
    

    def makeIntensity(self):

        self.axes = []
        for i in reversed(range(len(self.all_data))):
            time = self.all_data[i]["time"]
            donor = self.all_data[i]["donor"]
            acceptor = self.all_data[i]["acceptor"]
            ax = self.fig.add_subplot(len(self.all_data), 2, 2*i+1)
            ax.plot(time, donor, color=self.color1, label="Donor")
            ax.plot(time, acceptor, color=self.color2, label="Acceptor")
            ax.set_ylim([self.ymin, self.ymax]) #should be able to standardize this across a set?
            ax.set_xlim([self.xmin, self.xmax])
            ax.set_xticks([])
            #ax.set_title(self.title)
            self.axes.append(ax)
        
        self.axes[0].xaxis.set_major_locator(plt.AutoLocator())

        #f.annotate(text=self.title, xy=(0.03, 0.05), xycoords='axes fraction') #toggle on and off
        #self.fig.subplots_adjust(wspace=0, hspace=0, left=0.25, right=0.9)
        # remove x-tick labels on subplots, except for last one
        for i in range(1, len(self.all_data)):
           self.axes[i].xaxis.set_major_locator(plt.AutoLocator())
           self.axes[i].set_xticklabels([])

        self.axes[0].set_xlabel(self.xlabel, fontsize=self.xfontsize)
        #self.fig.supylabel("Intensity (AU)", fontsize=12, x=0.1)
        self.fig.text(0.1, 0.5, self.ylabel, ha="left", va="center", rotation="vertical", fontsize=self.yfontsize)


    
    def makeEfficiency(self):
        self.Eaxes = []
        for i in reversed(range(len(self.all_data))):
            time = self.all_data[i]["time"]
            efret = self.all_data[i]["efret"]

            ax = self.fig.add_subplot(len(self.all_data), 2, 2*(i+1))
            ax.plot(time, efret, color=self.color3)
            ax.set_ylim([self.y2min, self.y2max]) 
            #ax.set_title(self.title)
            ax.set_xlim([self.xmin, self.xmax])
            ax.set_xticks([])
            self.Eaxes.append(ax)
        
        self.Eaxes[0].xaxis.set_major_locator(plt.AutoLocator())

        #f.annotate(text=self.title, xy=(0.03, 0.05), xycoords='axes fraction') #toggle on and off
    
        # remove x-tick labels on subplots, except for last one
        for i in range(1, len(self.all_data)):
           self.Eaxes[i].xaxis.set_major_locator(plt.AutoLocator())
           self.Eaxes[i].set_xticklabels([])

        self.Eaxes[0].set_xlabel(self.x2label, fontsize=self.x2fontsize)
        #self.fig.supylabel("FRET Efficiency", fontsize=12, x=0.5)
        self.fig.text(0.525, 0.5, self.y2label, ha="left", va="center", rotation="vertical", fontsize=self.y2fontsize)

        
    
    def processData(self):
        max_donor_data = 0
        max_acceptor_data = 0
        max_time = 0
        for data in self.all_data:
            if data["donor"].max() > max_donor_data:
                max__donor_data = data["donor"].max()
            if data["acceptor"].max() > max_acceptor_data:
                max_acceptor_data = data["acceptor"].max()
            if data["time"].max() > max_time:
                max_time = data["time"].max()
        self.max_data = max(max_donor_data, max_acceptor_data)
        self.maxtime = max_time

    def save(self, refpath, reftype, refqual):
        if refqual == "Low":
            dpi=200
        elif refqual == "Medium":
            dpi=400
        elif refqual == "High":
            dpi=600
        refpath += reftype
        self.fig.savefig(refpath, dpi=dpi)
       #self.annotate(refpath)
        print("SAVED!")

    def destroy(self):
        self.trajectorycanvas.get_tk_widget().destroy()