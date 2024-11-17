from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure


class TrajectoryMaker():

    # title is the full file path
    # title set is the window title aka the parent folder that was inputted
    # data should come in as a dataframe
    def __init__(self, title, titleset, data, master, refcolor1, refcolor2, refcolor3, graphtitle, graphtitlefontsize, x, xfontsize,
                 x2, x2fontsize, y, yfontsize, y2, y2fontsize, height, width, xmax, xmin, ymax, ymin, y2max, y2min):
        self.data = data
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

        self.xmax = xmax
        self.xmin = xmin
        self.ymax = ymax
        self.ymin = ymin
        self.y2max = y2max
        self.y2min = y2min



        keys = title.split("/")
        self.title = ""
        count = False
        for i in range(len(keys)):
            if count:
                self.title += "/" + keys[i]
            if keys[i] == titleset:
                count = True

        self.title = self.title.split(".")[0]
        self.title = self.title.strip("/")

        self.fig = Figure()

        self.fig.set_figwidth(self.width)
        self.fig.set_figheight(self.height)

        self.axes = []
        for i in range(2):
            ax = self.fig.add_subplot(2, 1, i+1)
            self.axes.append(ax)
            

        self.makeIntensity()
        self.makeEfficiency()

        self.fig.subplots_adjust(wspace=0, hspace=0.5, left=0.1, right=0.9)
        self.fig.suptitle(self.graphtitle, fontsize=self.titlefontsize)

        self.trajectorycanvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.trajectorycanvas.draw()
        self.trajectorycanvas.get_tk_widget().grid(row=0, column=0)



    def makeIntensity(self):
        fig = self.axes[0]
        #f = fig.gca()
        
        time = self.data["time"]
        donor = self.data["donor"]
        acceptor = self.data["acceptor"]

        fig.plot(time, donor, color=self.color1, label="Donor")
        fig.plot(time, acceptor, color=self.color2, label="Acceptor")
        
        fig.legend()
        #fig.set_title("Intensity")
        fig.set_xlabel(self.xlabel, fontsize=self.xfontsize)
        fig.set_ylabel(self.ylabel, fontsize=self.yfontsize)
        fig.set_xlim([self.xmin, self.xmax])
        fig.set_ylim([self.ymin, self.ymax])
        fig.annotate(text=self.title, xy=(0.03, 0.05), xycoords='axes fraction') #toggle on and off
        #fig.tight_layout()

        return fig
    
    def makeEfficiency(self):
        fig = self.axes[1]
        #f = fig.gca()
        
        time = self.data["time"]
        efret = self.data["efret"]

        fig.plot(time, efret, color=self.color3)
        fig.set_ylim([0, 1]) 
        fig.set_ylabel(self.y2label, fontsize=self.y2fontsize)
        fig.set_xlabel(self.x2label, fontsize=self.x2fontsize)
        fig.set_xlim([self.xmin, self.xmax])
        fig.set_ylim([self.y2min, self.y2max])
        #fig.set_title("FRET Efficiency")
        fig.annotate(text=self.title, xy=(0.03, 0.05), xycoords='axes fraction') #toggle on and off
        #fig.tight_layout()
        
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
       #self.annotate(refpath)
        print("SAVED!")

    # removes canvas
    def destroy(self):
        self.trajectorycanvas.get_tk_widget().destroy()