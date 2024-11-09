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

        self.intensityfig = self.makeIntensity()
        self.efficiencyfig = self.makeEfficiency()

    def makeIntensity(self):
        fig = Figure(dpi=80)
        fig.set_figwidth(6)
        fig.set_figheight(3)
        f = fig.gca()
        
        time = self.data["time"]
        donor = self.data["donor"]
        acceptor = self.data["acceptor"]

        f.plot(time, donor, color="lime", label="Donor")
        f.plot(time, acceptor, color="red", label="Acceptor")
        f.set_ylim([0, None]) #should be able to standardize this across a set?
        f.legend()
        f.set_title("Intensity")
        f.annotate(text=self.title, xy=(0.03, 0.05), xycoords='axes fraction') #toggle on and off
        fig.tight_layout()
        
        trajectorycanvas = FigureCanvasTkAgg(fig, master=self.master)
        trajectorycanvas.draw()
        trajectorycanvas.get_tk_widget().grid(row=0, column=0)
        return fig
    
    def makeEfficiency(self):
        fig = Figure(dpi=80)
        fig.set_figwidth(6)
        fig.set_figheight(3)
        f = fig.gca()
        
        time = self.data["time"]
        efret = self.data["efret"]

        f.plot(time, efret, color="black")
        f.set_ylim([0, 1]) 
        f.set_title("FRET Efficiency")
        f.annotate(text=self.title, xy=(0.03, 0.05), xycoords='axes fraction') #toggle on and off
        fig.tight_layout()
        
        trajectorycanvas = FigureCanvasTkAgg(fig, master=self.master)
        trajectorycanvas.draw()
        trajectorycanvas.get_tk_widget().grid(row=1, column=0)
        return fig