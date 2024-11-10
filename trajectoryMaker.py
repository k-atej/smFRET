from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure


class TrajectoryMaker():

    # title is the full file path
    # title set is the window title aka the parent folder that was inputted
    # data should come in as a dataframe
    def __init__(self, title, titleset, data, master):
        self.data = data
        self.master = master


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
        self.fig.set_figwidth(6)
        self.fig.set_figheight(4.5)
        self.axes = []
        for i in range(2):
            ax = self.fig.add_subplot(2, 1, i+1)
            self.axes.append(ax)
            

        self.makeIntensity()
        self.makeEfficiency()

        self.fig.subplots_adjust(wspace=0, hspace=0.5, left=0.1, right=0.9)

        trajectorycanvas = FigureCanvasTkAgg(self.fig, master=self.master)
        trajectorycanvas.draw()
        trajectorycanvas.get_tk_widget().grid(row=0, column=0)



    def makeIntensity(self):
        fig = self.axes[0]
        #f = fig.gca()
        
        time = self.data["time"]
        donor = self.data["donor"]
        acceptor = self.data["acceptor"]

        fig.plot(time, donor, color="lime", label="Donor")
        fig.plot(time, acceptor, color="red", label="Acceptor")
        fig.set_ylim([0, None]) #should be able to standardize this across a set?
        fig.legend()
        fig.set_title("Intensity")
        fig.annotate(text=self.title, xy=(0.03, 0.05), xycoords='axes fraction') #toggle on and off
        #fig.tight_layout()

        return fig
    
    def makeEfficiency(self):
        fig = self.axes[1]
        #f = fig.gca()
        
        time = self.data["time"]
        efret = self.data["efret"]

        fig.plot(time, efret, color="black")
        fig.set_ylim([0, 1]) 
        fig.set_title("FRET Efficiency")
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