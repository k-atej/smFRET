from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
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
#   - subtitles: labels applied to each subfigure
#   - subtitlesizes: size of each label for each subfigure
#   - linesize1, 2, & 3: linewidths for each plot
class StackedTrajectoryMaker():

    # initializes the variables within the class
    def __init__(self, all_data, master, title, files, refcolor1, refcolor2, refcolor3, 
                 graphtitle, graphtitlesize, x, xfontsize, x2, x2fontsize, y, yfontsize, y2, y2fontsize, 
                 height, width, xmax, xmin, y2max, y2min, intensitytoggle, efficiencytoggle,
                 legendtoggle, subtitletoggle, subtitletoggle2, yshift, eyshift, clicktogg,
                 subtitles, subtitlesizes, linesize1, linesize2, linesize3, yaxes, ymaxes, ymins, y2ticks):
        # designate data
        self.all_data = all_data
        self.yshift = yshift
        self.eyshift = eyshift
        self.datacopy = []

        for i in range(len(self.all_data)):
            datum = self.all_data[i]
            datumcopy = datum.copy()
            self.datacopy.append(datumcopy)
            datumcopy['donor'] = datumcopy['donor'] - self.yshift[i]
            datumcopy['acceptor'] = datumcopy['acceptor'] - self.yshift[i]
            datumcopy['efret'] = datumcopy['efret'] - self.eyshift[i] # why is this returning as an object?

        # set subtitles
        self.subtitles = subtitles
        self.subtitlesizes = subtitlesizes

        # set colors for graph
        self.color1 = refcolor1
        self.color2 = refcolor2
        self.color3 = refcolor3

        # set text & text sizes for graph
        self.master = master
        self.title = title
        self.files = files
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

        # set toggles
        self.intensitytoggle = intensitytoggle
        self.efficiencytoggle = efficiencytoggle
        self.legend = legendtoggle
        self.subtitle = subtitletoggle
        self.subtitle2 = subtitletoggle2
        self.clicktoggle = clicktogg

        # set axis variables
        self.y2ticks = y2ticks
        if self.y2ticks == "":
            self.y2ticks = [0.0, 0.5, 1.0]
            temp = []
            for val in self.y2ticks:
                val = float(val)
                val = round(val, 1)
                temp.append(val)
            self.y2ticks = temp
        


        self.xmaxes = xmax
        self.xmins = xmin
        self.y2max = y2max
        self.y2min = y2min
        self.iaxes = None
        self.eaxes = None
        self.yaxes = yaxes
        self.ymaxes = ymaxes
        self.ymins = ymins

        # set linewidths
        self.linewidth1 = linesize1
        self.linewidth2 = linesize2
        self.linewidth3 = linesize3

        # set figure dimensions
        self.width = width
        self.height = height

        self.yticklabels = []
        self.ymaxlbls = []
        self.yminlbls = []
        self.xmaxlbls = []
        self.xminlbls = []
        self.axes = []
        self.Eaxes = []

        self.start()
    
    # generate graphs and add to figure
    def start(self):
        # configure size of figure
        self.fig = Figure()
        self.fig.set_figwidth(self.width)
        self.fig.set_figheight(self.height)

        # parse data
        self.processData()
        

        # toggle updates
        #if self.xmax == None:
         #   self.xmax = self.maxtime
        self.numdata = 0
        if self.intensitytoggle == 1:
            self.numdata += 1
        if self.efficiencytoggle == 1:
            self.numdata += 1
        
        bottompad = 0.1
        if self.height >= 3.9:
            heightpad = 0.9
        elif self.height >= 3.2:
            heightpad = 0.875
        else:
            heightpad = 0.85
            if self.height <= 2:
                bottompad = 0.25
                if self.height <=1:
                    bottompad = 0.4
        self.leftpad = 0
        if self.width <= 5:
            self.leftpad = 0.1
        
        # make subplots
        if self.intensitytoggle == 1:
            self.makeIntensity()
        if self.efficiencytoggle == 1:
            self.makeEfficiency()
    
        
        # configure the canvas containing the subplots
        self.fig.subplots_adjust(wspace=(0.4 + self.leftpad), hspace=0, left=(0.2 + self.leftpad), right=0.95, top=heightpad, bottom=((1.0-heightpad)+bottompad))
        self.fig.suptitle(self.title, y=0.95, x=0.55, fontsize=self.titlefontsize)  
        self.trajectorycanvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.trajectorycanvas.draw()
        self.trajectorycanvas.get_tk_widget().grid(row=0, column=0, padx=(5, 5))

        # connect clicks to zeroing
        self.fig.canvas.mpl_connect('button_press_event', lambda event: self.onclick(event))
        self.restore_axes()

        
    
    # generate fluorophore intensity graph
    def makeIntensity(self):
        
        # configure axes for each plot
        for i in reversed(range(len(self.all_data))):
            # set variables 
            time = self.datacopy[i]["time"]
            donor = self.datacopy[i]["donor"]
            acceptor = self.datacopy[i]["acceptor"]
            
            # plot data
            ax = self.fig.add_subplot(len(self.all_data), self.numdata, self.numdata*i+1)
            ax.plot(time, donor, color=self.color1, label="Donor", linewidth=self.linewidth1)
            ax.plot(time, acceptor, color=self.color2, label="Acceptor", linewidth=self.linewidth2)
            
            # axis options
            self.xlim = ax.get_xlim()
            self.ylim = ax.get_ylim()
            
            # STILL WORKSHOPPING THIS: USERS MAY NEED TO SPECIFY WHICH TICKS TO SHOW?
            if len(self.yaxes) == 0:
                tick = ax.get_yticks()
                temp = []
                for val in tick:
                    val = float(val)
                    val = round(val, 1)
                    temp.append(val)
                self.yticklabels.append(temp)
                ax.set_yticks(temp)
                ymin, ymax = ax.get_ylim()
                self.ymaxlbls.append(ymax)
                self.yminlbls.append(ymin)
                xmin, xmax = ax.get_xlim()
                self.xmaxlbls.append(xmax)
                self.xminlbls.append(xmin)
                self.xmaxlbls = self.xmaxlbls[::-1]
                self.xminlbls = self.xminlbls[::-1]
            else:
                self.ymaxlbls = self.ymaxes
                self.yticklabels = self.yaxes
                self.yminlbls = self.ymins
                self.xmaxlbls = self.xmaxes
                self.xminlbls = self.xmins

            
            # subtitles
            if self.subtitle == 1:
                key = os.path.basename(self.files[i])
                if len(self.subtitles) != 0:
                    ax.annotate(text=self.subtitles[i], fontsize=self.subtitlesizes[i], xy=(0.03, 0.8), xycoords='axes fraction')
                else:
                    ax.annotate(text=key.split(".")[0], fontsize=9, xy=(0.03, 0.8), xycoords='axes fraction')
            
            self.axes.append(ax)
       
        # share axes between figures
        for ax in self.axes:
            ax.tick_params(axis="x", which="both", labelbottom=False)
        self.axes[0].set_xlabel(self.xlabel, fontsize=self.xfontsize)
        self.axes[0].tick_params(axis="x", which="both", labelbottom=True)
        
        # toggles
        if self.legend ==1:
            self.axes[len(self.all_data) - 1].legend() 
        if self.intensitytoggle == 1:
            self.fig.text((0.05 + self.leftpad/2), 0.5, self.ylabel, ha="left", va="center", rotation="vertical", fontsize=self.yfontsize)

        self.axes.reverse()


    def get_yticks(self):
        return self.yticklabels
    
    def get_ymaxes(self):
        return self.ymaxlbls
    
    def get_ymins(self):
        return self.yminlbls
    
    def get_xmins(self):
        return self.xminlbls

    def get_xmaxes(self):
        return self.xmaxlbls
    
    def restore_axes(self):
        if len(self.axes) == len(self.yaxes):
            i = 0
            for ax in self.axes:
                tix = []
                temp = self.yaxes[i]
                temp = temp.strip()
                temp = temp.strip(",")
                temp = temp.strip()
                temp = temp.split(",")

                val2 = float(self.ymaxes[i])
                val3 = float(self.ymins[i])
                for val in temp:
                    val = val.strip()
                    val = float(val)
                    val = round(val, 1)
                    tix.append(val)
                ax.set_yticks(tix)
                ax.set_ylim([val3, val2])
                val4 = self.xmins[i]
                val5 = self.xmaxes[i]
                val4 = float(val4)
                val4 = round(val4, 1)
                val5 = float(val5)
                val5 = round(val5, 1)
                ax.set_xlim([val4, val5])
                i += 1

        if len(self.Eaxes) == len(self.yaxes):
            i = 0
            for ax in self.Eaxes:
                val4 = self.xmins[i]
                val5 = self.xmaxes[i]
                val4 = float(val4)
                val4 = round(val4, 1)
                val5 = float(val5)
                val5 = round(val5, 1)
                ax.set_xlim([val4, val5])
                i += 1

    
    # generate FRET efficiency graph
    def makeEfficiency(self):

        # configure axes for each plot
        for i in reversed(range(len(self.all_data))):
            # set variables 
            time = self.datacopy[i]["time"]
            efret = self.datacopy[i]["efret"]

            # plot data
            ax = self.fig.add_subplot(len(self.all_data), self.numdata, self.numdata*(i+1))
            ax.plot(time, efret, color=self.color3, linewidth=self.linewidth3)

            # set ticks for y-axis
            ax.set_yticks(self.y2ticks)
            ax.set_ylim([self.y2min, self.y2max]) 

            # subtitles
            if self.subtitle2 == 1:
                key = os.path.basename(self.files[i])

                if len(self.subtitles) != 0:
                    ax.annotate(text=self.subtitles[i], fontsize=self.subtitlesizes[i], xy=(0.03, 0.8), xycoords='axes fraction')
                else:
                    ax.annotate(text=key.split(".")[0], fontsize=9, xy=(0.03, 0.8), xycoords='axes fraction')
            
  
            self.Eaxes.append(ax)

        # shared axis options
        self.y2min, self.y2max = self.Eaxes[0].get_ylim()
        for ax in self.Eaxes:
            ax.tick_params(axis="x", which="both", labelbottom=False)
        self.Eaxes[0].set_xlabel(self.x2label, fontsize=self.x2fontsize)
        self.Eaxes[0].tick_params(axis="x", which="both", labelbottom=True)
        

        
        if self.numdata == 2:
            self.fig.text((0.53+self.leftpad/2), 0.5, self.y2label, ha="left", va="center", rotation="vertical", fontsize=self.y2fontsize)
        else:
            self.fig.text((0.05 + self.leftpad/2), 0.5, self.y2label, ha="left", va="center", rotation="vertical", fontsize=self.y2fontsize)
        self.Eaxes.reverse()


    # combs through data to find bounds
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

    # return x and y limit for both the fluorophore intensity and FRET efficiency graphs
    def getMinMax(self):
        return self.y2min, self.y2max, self.y2ticks

    # calculate FRET efficiency
    def calculateEfret(self):
        for data in self.datacopy:
            gamma = GAMMA
            data['efret'] = data['acceptor'] / (data['acceptor'] + (gamma * data['donor']))
    
    # return y shift
    def getShift(self):
        return self.yshift, self.eyshift
    
    # set y shift
    def setShift(self, yshift, eyshift):
        for i in range(len(self.yshift)):
            self.yshift[i] = yshift
            self.eyshift[i] = eyshift
    
    # handles all click events
    def onclick(self, event):
        if self.clicktoggle == 1:
            if event.inaxes:
                for i in range(len(self.axes)):
                    if event.inaxes == self.axes[i]: # will need to make this specific to each intensity subgraph
                        self.yshift[i] += event.ydata
                        self.datacopy[i]['donor'] = self.datacopy[i]['donor'] - event.ydata
                        self.datacopy[i]['acceptor'] = self.datacopy[i]['acceptor'] - event.ydata
                        self.start()
                    elif event.inaxes == self.Eaxes[i]: # will need to make this specific to each intensity subgraph
                        self.eyshift[i] += event.ydata
                        self.datacopy[i]['efret'] = self.datacopy[i]['efret'] - event.ydata
                        self.start()

    # return number of plots in stacked histogram
    def get_height(self):
        return len(self.all_data)
    
    # return list of subtitles on histogram
    def get_subtitles(self):
        return self.subtitles
    
    # return name of last folder in filepath
    def get_lastfolder(self):
        return self.lastFolder
    
    # return list of subtitle sizes on histogram
    def get_subtitlesizes(self):
        return self.subtitlesizes
    
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
        #path: {self.title} full file path ?
        text = f"""
        data: {self.all_data}
        
        files: {self.files}
        title: {self.title}
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
        x-axis maxes: {self.xmaxlbls}
        x-axis mins: {self.xminlbls}
        y-axis 2 max: {self.y2max}
        y-axis 2 min: {self.y2min}
        e ticks: {self.y2ticks}
        i ticks: {self.yticklabels}
        i maxes: {self.ymaxlbls}
        i mins: {self.yminlbls}
        
        offset: {self.yshift, self.eyshift}
        legend: {self.legend}
        figure width: {self.width}
        figure height: {self.height} 

        intensity plot: {self.intensitytoggle}
        efficiency plot: {self.efficiencytoggle}
        subtitles:{self.subtitles}
        subtitle sizes: {self.subtitlesizes}

        """
        return text