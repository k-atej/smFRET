from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
from matplotlib import pyplot as plt


class StackedTrajectoryMaker():

    # title is the full file path
    # title set is the window title aka the parent folder that was inputted
    # data should come in as a dataframe
    def __init__(self, all_data, master, title):
        self.all_data = all_data
        self.master = master
        self.title = title

        self.intensityfig = self.makeIntensity()
        self.efficiencyfig = self.makeEfficiency()

    def makeIntensity(self):
        self.processData()

        fig = Figure(dpi=80)
        fig.set_figwidth(4.5)
        fig.set_figheight(5.5)
        
        time = self.all_data[0]["time"]
        donor = self.all_data[0]["donor"]
        acceptor = self.all_data[0]["acceptor"]

        self.axes = []
        for i in reversed(range(len(self.all_data))):
            time = self.all_data[i]["time"]
            donor = self.all_data[i]["donor"]
            acceptor = self.all_data[i]["acceptor"]

            ax = fig.add_subplot(len(self.all_data), 1, i+1)
            ax.plot(time, donor, color="lime", label="Donor")
            ax.plot(time, acceptor, color="red", label="Acceptor")
            ax.set_ylim([0, self.max_data + 100]) #should be able to standardize this across a set?
            ax.set_xlim([0, None])
            ax.set_xticks([])
            #ax.set_title(self.title)
            self.axes.append(ax)
        
        self.axes[0].xaxis.set_major_locator(plt.AutoLocator())

        #f.annotate(text=self.title, xy=(0.03, 0.05), xycoords='axes fraction') #toggle on and off
        fig.subplots_adjust(wspace=0, hspace=0, left=0.25, right=0.9)
        # remove x-tick labels on subplots, except for last one
        for i in range(1, len(self.all_data)):
           self.axes[i].xaxis.set_major_locator(plt.AutoLocator())
           self.axes[i].set_xticklabels([])

        self.axes[0].set_xlabel("Time", fontsize=12)
        fig.supylabel("Intensity (AU)", fontsize=12, x=0.1)
        fig.suptitle(self.title, y = 0.93, x=0.57, fontsize=12)

        trajectorycanvas = FigureCanvasTkAgg(fig, master=self.master)
        trajectorycanvas.draw()
        trajectorycanvas.get_tk_widget().grid(row=0, column=0, padx=(5, 5))
        return fig
    
    def makeEfficiency(self):
        fig = Figure(dpi=80)
        fig.set_figwidth(4.5)
        fig.set_figheight(5.5)
        
        time = self.all_data[0]["time"]
        efret = self.all_data[0]["efret"]


        self.Eaxes = []
        for i in reversed(range(len(self.all_data))):
            ax = fig.add_subplot(len(self.all_data), 1, i+1)
            ax.plot(time, efret, color="black")
            ax.set_ylim([0, 1.3]) 
            #ax.set_title(self.title)
            ax.set_xlim([0, None])
            ax.set_xticks([])
            self.Eaxes.append(ax)
        
        self.Eaxes[0].xaxis.set_major_locator(plt.AutoLocator())

        #f.annotate(text=self.title, xy=(0.03, 0.05), xycoords='axes fraction') #toggle on and off
        fig.subplots_adjust(wspace=0, hspace=0, left=0.25, right=0.9)
        # remove x-tick labels on subplots, except for last one
        for i in range(1, len(self.all_data)):
           self.Eaxes[i].xaxis.set_major_locator(plt.AutoLocator())
           self.Eaxes[i].set_xticklabels([])

        self.Eaxes[0].set_xlabel("Time", fontsize=12)
        fig.supylabel("FRET Efficiency", fontsize=12, x=0.1)
        fig.suptitle(self.title, y = 0.93, x=0.57, fontsize=12)

        #f.annotate(text=self.title, xy=(0.03, 0.05), xycoords='axes fraction') #toggle on and off
        
        trajectorycanvas = FigureCanvasTkAgg(fig, master=self.master)
        trajectorycanvas.draw()
        trajectorycanvas.get_tk_widget().grid(row=0, column=1, padx=(5, 5))
        return fig
    
    def processData(self):
        max_donor_data = 0
        max_acceptor_data = 0
        for data in self.all_data:
            if data["donor"].max() > max_donor_data:
                max__donor_data = data["donor"].max()
            if data["acceptor"].max() > max_acceptor_data:
                max_acceptor_data = data["acceptor"].max()
        self.max_data = max(max_donor_data, max_acceptor_data)
