import pandas as pd
import tkinter as tk
from histograms.histogramMaker import *
from histograms.histogramWindow import *
from histograms.stackedHistogramWindow import *
from trajectories.trajectoryMaker import *
from trajectories.stackedTrajectoryMaker import *

GAMMA = 1.0
# creates the window containing the customization menu & the graphs
#   - path: what the user inputted into the window
#   - file: fill file paths for each of the designated files in folder
#   - filetype: what kind of file the program was initially looking for
class stackedTrajectoryWindow(tk.Toplevel):

    # initializes the variables within the class
    def __init__(self, path, files, filetype):
        super().__init__()
        self.minsize(200, 200)
        self.path = path  # what the user input into the box in the menu
        self.type = filetype
        self.files = files  # list of filepaths for every trace file found within the folder
        self.figtitle = os.path.basename(self.path)
        self.title(self.figtitle)

        self.trajectory = None
        self.generation = 0
        self.yshift = []
        self.eyshift = []
        self.subtitle_inputs = []
        self.yaxis_inputs = []
        self.xaxis_inputs = []
        for file in files:
            self.yshift.append(0.0)
            self.eyshift.append(0.0)

        #full window 
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)

        #area above the intensity viewer
        self.subframetop = tk.Frame(self.frame, background='white')
        self.subframetop.grid(row=0, column=0, columnspan=2)

        # left half (contains intensities and efret figures)
        self.subframeleft = tk.Frame(self.frame, background='white')
        self.subframeleft.grid(row=1, column=0)

        # right half (contains menu)
        self.subframeright = tk.Frame(self.frame, background='white')
        self.subframeright.grid(row=1, column=1)

        # right half, top (contains i menu)
        self.subframerighttop = tk.Frame(self.subframeright, background='white')
        self.subframerighttop.grid(row=0, column=0)

        # right half, bottom (contains e menu)
        self.subframerightbottom = tk.Frame(self.subframeright, background='white')
        self.subframerightbottom.grid(row=1, column=0)

        self.start()

    # create window, menus, and trajectory graphs
    def start(self):

        # set up customization menu
        self.makeFormat()
        self.makeButtons()
        self.makeOptions() 

        # create the graphs and paste into window
        self.maketrajectory()

        # binds keys to functions
        self.bind('<BackSpace>', self.undo)
        self.bind('<Return>', self.maketrajectory)

    # set up buttons at the top of window
    def makeButtons(self):
        # generate button, bound to the generation of a histogram
        makeTraj = tk.Button(self.subframetop, text="Generate", command=self.maketrajectory)
        makeTraj.grid(row=0, column=0, padx="10")

        # save button
        self.saveButton = tk.Button(self.subframetop, text="Save", command=self.savewindow)
        self.saveButton.grid(row=0, column=1, sticky="ew", padx="10", pady="10")

        # click-to-zero toggle
        self.sub3togg = tk.IntVar()
        self.togglesub3 = tk.Checkbutton(self.subframetop, text="Click to Zero", variable=self.sub3togg, onvalue=1, offvalue=0)
        self.togglesub3.grid(row=0, column=2, sticky="ew", padx="10", pady="10")
        self.sub3togg.set(0)
    
    # set up tabular menu on side of window
    def makeFormat(self):
        self.tabControl = ttk.Notebook(master=self.subframerighttop)
        self.tabFormat = tk.Frame(self.tabControl)
        self.tabControl.grid(row=0, column=0, rowspan=2, padx=10, sticky='n')

        self.tabFormat = tk.Frame(self.tabControl)
        self.tabStyle = tk.Frame(self.tabControl)
        self.tabText = tk.Frame(self.tabControl)
        self.tabSub = tk.Frame(self.tabControl)
        self.tabAxes = tk.Frame(self.tabControl)

        self.tabControl.add(self.tabFormat, text="Format")
        self.tabControl.add(self.tabAxes, text="Y-Axes")
        self.tabControl.add(self.tabStyle, text="Style")
        self.tabControl.add(self.tabText, text="Text")
        self.tabControl.add(self.tabSub, text="Subtitles")

    # insert options into tabular window
    def makeOptions(self):
        # tab 1: format
         # input area to designate maximum value on x axis
        #check box for toggling to bin width input
        self.intensitytogg = tk.IntVar()
        self.toggle1 = tk.Checkbutton(self.tabFormat, text="Intensity Plot", variable=self.intensitytogg, onvalue=1, offvalue=0)
        self.toggle1.grid(row=3, column=0, sticky="ew", padx=(10,10), pady=(10,5), columnspan=2)
        self.intensitytogg.set(1)

        # checkbox for displaying the efficiency plot
        self.efficiencytogg = tk.IntVar()
        self.toggle2 = tk.Checkbutton(self.tabFormat, text="Efficiency Plot", variable=self.efficiencytogg, onvalue=1, offvalue=0)
        self.toggle2.grid(row=4, column=0, sticky="ew", padx=(10,10), pady=(10,5), columnspan=2)
        self.efficiencytogg.set(1)

        '''
        # input area to designate maximum value on x axis
        self.xmax_label = tk.Label(self.tabFormat, text="X Max:")
        self.xmax_label.grid(row=5, column=2, pady="5")
        self.ref_xmax = tk.StringVar(self)
        self.ref_xmax.set("None")

        self.comboxmax = tk.Entry(self.tabFormat, textvariable=self.ref_xmax)
        self.comboxmax.config(width=9)
        self.comboxmax.grid(row=5, column=3, sticky="ew", padx=(0, 10), pady="5")

        # input area to designate minimum value on x axis
        self.xmin_label = tk.Label(self.tabFormat, text="X Min:")
        self.xmin_label.grid(row=5, column=0, padx=(20,0), pady="5")
        self.ref_xmin = tk.StringVar(self)
        self.ref_xmin.set("0")

        self.comboxmin = tk.Entry(self.tabFormat, textvariable=self.ref_xmin)
        self.comboxmin.config(width=9)
        self.comboxmin.grid(row=5, column=1, sticky="ew", padx=(0, 10), pady="5")
        '''
        '''
        # input area to designate maximum value on y axis
        self.ymax_label = tk.Label(self.tabFormat, text="Y Max:")
        self.ymax_label.grid(row=5, column=2, pady="5")
        self.ref_ymax = tk.StringVar(self)
        self.ref_ymax.set("None")

        self.comboymax = tk.Entry(self.tabFormat, textvariable=self.ref_ymax)
        self.comboymax.config(width=5)
        self.comboymax.grid(row=5, column=3, sticky="ew", padx=(0, 10), pady="5")

        # input area to designate minimum value on y axis
        self.ymin_label = tk.Label(self.tabFormat, text="Y Min:")
        self.ymin_label.grid(row=5, column=0, padx=(20,0), pady="5")
        self.ref_ymin = tk.StringVar(self)
        self.ref_ymin.set("0")

        self.comboymin = tk.Entry(self.tabFormat, textvariable=self.ref_ymin)
        self.comboymin.config(width=5)
        self.comboymin.grid(row=5, column=1, sticky="ew", padx=(0, 10), pady="5")
        '''


        # input area for figure width
        self.width_label = tk.Label(self.tabFormat, text="Width:")
        self.width_label.grid(row=1, column=0, padx=(20,0), pady="5")
        self.ref_width = tk.StringVar(self)
        self.ref_width.set('6')

        self.combowidth = tk.Entry(self.tabFormat, textvariable=self.ref_width)
        self.combowidth.config(width=5)
        self.combowidth.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="5")

         # input area for figure height
        self.height_label = tk.Label(self.tabFormat, text="Height:")
        self.height_label.grid(row=2, column=0, padx=(20,0), pady="5")
        self.ref_height = tk.StringVar(self)
        self.ref_height.set('4.5')

        self.comboheight = tk.Entry(self.tabFormat, textvariable=self.ref_height)
        self.comboheight.config(width=5)
        self.comboheight.grid(row=2, column=1, sticky="ew", padx=(0, 10), pady="5")


        # tab2 : style

        self.i_label = tk.Label(self.tabStyle, text="Intensity Plot:")
        self.i_label.grid(row=0, column=0, columnspan=2, pady=(10,5), sticky="w")

        # legend toggle
        self.legendtogg = tk.IntVar()
        self.togglelegend = tk.Checkbutton(self.tabStyle, text="Legend", variable=self.legendtogg, onvalue=1, offvalue=0)
        self.togglelegend.grid(row=1, column=0, sticky="ew", padx=(20, 0), pady="5")
        self.legendtogg.set(1)

         # input area for designation of plot1 color
        self.color_label = tk.Label(self.tabStyle, text="Donor:")
        self.color_label.grid(row=2, column=0)
        self.ref_color1 = tk.StringVar(self)
        self.ref_color1.set("lime")

        self.combo2 = tk.Entry(self.tabStyle, textvariable=self.ref_color1)
        self.combo2.config(width=5)
        self.combo2.grid(row=2, column=1, sticky="ew", padx=(0, 10), pady="5")

        # color wheel for designation of plot1 color
        self.color1button = tk.Button(self.tabStyle, text="Select Color", command=self.choose_plotAcolor)
        self.color1button.grid(row=2, column=3)

        # dropdown for plot1 line size
        linex = [0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        self.ref_linesize = tk.StringVar(self)
        self.ref_linesize.set("1.5")

        self.line4 = tk.OptionMenu(self.tabStyle, self.ref_linesize, *linex)
        self.line4.config(width=1)
        self.line4.grid(row=2, column=4, pady="5")

        
        # input area for designation of plot2 color
        self.color_label = tk.Label(self.tabStyle, text="Acceptor:")
        self.color_label.grid(row=3, column=0, padx=(15,0))
        self.ref_color2 = tk.StringVar(self)
        self.ref_color2.set("red")

        self.combo3 = tk.Entry(self.tabStyle, textvariable=self.ref_color2)
        self.combo3.config(width=5)
        self.combo3.grid(row=3, column=1, sticky="ew", padx=(0, 10), pady="5")

        # color wheel for designation of plot2 color
        self.color2button = tk.Button(self.tabStyle, text="Select Color", command=self.choose_plotBcolor)
        self.color2button.grid(row=3, column=3)

        # dropdown for plot2 line size
        linex2 = [0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        self.ref_linesize2 = tk.StringVar(self)
        self.ref_linesize2.set("1.5")

        self.line5 = tk.OptionMenu(self.tabStyle, self.ref_linesize2, *linex2)
        self.line5.config(width=1)
        self.line5.grid(row=3, column=4, pady="5")

        self.e_label = tk.Label(self.tabStyle, text="Efficiency Plot:")
        self.e_label.grid(row=5, column=0, columnspan=2, pady=(10,5), sticky="w")



        # input area for designation of plot3 color
        self.color_label = tk.Label(self.tabStyle, text="Efficiency:")
        self.color_label.grid(row=6, column=0, padx=(20,0))
        self.ref_color3 = tk.StringVar(self)
        self.ref_color3.set("black")

        self.combo4 = tk.Entry(self.tabStyle, textvariable=self.ref_color3)
        self.combo4.config(width=5)
        self.combo4.grid(row=6, column=1, sticky="ew", padx=(0, 10), pady="5")

        # color wheel for designation of plot3 color
        self.color2button = tk.Button(self.tabStyle, text="Select Color", command=self.choose_plotCcolor)
        self.color2button.grid(row=6, column=3)

        # dropdown for plot3 line size
        linex3 = [0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        self.ref_linesize3 = tk.StringVar(self)
        self.ref_linesize3.set("1.5")

        self.line6 = tk.OptionMenu(self.tabStyle, self.ref_linesize3, *linex3)
        self.line6.config(width=1)
        self.line6.grid(row=6, column=4, pady="5")

        


        # third tab: text
        # all of these should be toggled on & off with each subplot, should toggle overall title individually

        # input area for designation of graph title
        self.title_label = tk.Label(self.tabText, text="Title:")
        self.title_label.grid(row=0, column=0)
        self.ref_title = tk.StringVar(self)
        self.ref_title.set(self.figtitle)

        self.combo2 = tk.Entry(self.tabText, textvariable=self.ref_title)
        self.combo2.config(width=15)
        self.combo2.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady="5")

        # dropdown for title font size
        self.titlef_label = tk.Label(self.tabText, text="Size:")
        self.titlef_label.grid(row=0, column=2)
        titlef = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
        self.ref_titlefontsize = tk.IntVar(self)
        self.ref_titlefontsize.set(12)

        self.combo = tk.OptionMenu(self.tabText, self.ref_titlefontsize, *titlef)
        self.combo.config(width=1)
        self.combo.grid(row=0, column=3)

        self.istyle_label = tk.Label(self.tabText, text="Intensity Plot:")
        self.istyle_label.grid(row=1, column=0, columnspan=2, pady=(10,5), sticky="w")

        self.estyle_label = tk.Label(self.tabText, text="Efficiency Plot:")
        self.estyle_label.grid(row=5, column=0, columnspan=2, pady=(10,5), sticky="w")

        # input area for designation of intensity x-axis label
        self.x_label = tk.Label(self.tabText, text="X-Axis:")
        self.x_label.grid(row=2, column=0, padx=(15,0))
        self.ref_x = tk.StringVar(self)
        self.ref_x.set("Time (s)")

        self.combo2 = tk.Entry(self.tabText, textvariable=self.ref_x)
        self.combo2.config(width=10)
        self.combo2.grid(row=2, column=1, sticky="ew", padx=(0, 10), pady="5")

        # input area for designation of efficiency x-axis label
        self.x2_label = tk.Label(self.tabText, text="X-Axis:")
        self.x2_label.grid(row=6, column=0, padx=(15,0))
        self.ref_x2 = tk.StringVar(self)
        self.ref_x2.set("Time (s)")

        self.combo2 = tk.Entry(self.tabText, textvariable=self.ref_x2)
        self.combo2.config(width=10)
        self.combo2.grid(row=6, column=1, sticky="ew", padx=(0, 10), pady="5")

        # input area for designation of intensity y-axis label
        self.y_label = tk.Label(self.tabText, text="Y-Axis:")
        self.y_label.grid(row=3, column=0, padx=(15,0))
        self.ref_y = tk.StringVar(self)
        self.ref_y.set("I (A.U.)")

        self.combo3 = tk.Entry(self.tabText, textvariable=self.ref_y)
        self.combo3.config(width=10)
        self.combo3.grid(row=3, column=1, sticky="ew", padx=(0, 10), pady="5")

        # input area for designation of efficiency y-axis label
        self.y2_label = tk.Label(self.tabText, text="Y-Axis:")
        self.y2_label.grid(row=7, column=0, padx=(15,0))
        self.ref_y2 = tk.StringVar(self)
        self.ref_y2.set("E_FRET")

        self.combo3 = tk.Entry(self.tabText, textvariable=self.ref_y2)
        self.combo3.config(width=10)
        self.combo3.grid(row=7, column=1, sticky="ew", padx=(0, 10), pady="5")

        # dropdown for x font size
        self.titlex_label = tk.Label(self.tabText, text="Size:")
        self.titlex_label.grid(row=2, column=2)
        titlex = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
        self.ref_xfontsize = tk.StringVar(self)
        self.ref_xfontsize.set("12")

        self.combo4 = tk.OptionMenu(self.tabText, self.ref_xfontsize, *titlex)
        self.combo4.config(width=1)
        self.combo4.grid(row=2, column=3)

        # dropdown for y font size
        self.titley_label = tk.Label(self.tabText, text="Size:")
        self.titley_label.grid(row=3, column=2)
        titley = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
        self.ref_yfontsize = tk.StringVar(self)
        self.ref_yfontsize.set("12")

        self.combo = tk.OptionMenu(self.tabText, self.ref_yfontsize, *titley)
        self.combo.config(width=1)
        self.combo.grid(row=3, column=3)

        # dropdown for x2 font size
        self.titlex2_label = tk.Label(self.tabText, text="Size:")
        self.titlex2_label.grid(row=6, column=2)
        titlex2 = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
        self.ref_x2fontsize = tk.StringVar(self)
        self.ref_x2fontsize.set("12")

        self.combo4 = tk.OptionMenu(self.tabText, self.ref_x2fontsize, *titlex2)
        self.combo4.config(width=1)
        self.combo4.grid(row=6, column=3)

        # dropdown for y2 font size
        self.titley2_label = tk.Label(self.tabText, text="Size:")
        self.titley2_label.grid(row=7, column=2)
        titley2 = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
        self.ref_y2fontsize = tk.StringVar(self)
        self.ref_y2fontsize.set("12")

        self.combo = tk.OptionMenu(self.tabText, self.ref_y2fontsize, *titley2)
        self.combo.config(width=1)
        self.combo.grid(row=7, column=3)

        # subtitle toggle: intensity
        self.subtogg = tk.IntVar()
        self.togglesub = tk.Checkbutton(self.tabText, text="Subtitles", variable=self.subtogg, onvalue=1, offvalue=0)
        self.togglesub.grid(row=4, column=0, sticky="ew", padx=(15,10), pady="5", columnspan=2)
        self.subtogg.set(1)

        # subtitle toggle: efficiency
        self.sub2togg = tk.IntVar()
        self.togglesub2 = tk.Checkbutton(self.tabText, text="Subtitles", variable=self.sub2togg, onvalue=1, offvalue=0)
        self.togglesub2.grid(row=8, column=0, sticky="ew", padx=(15,10), pady="5", columnspan=2)
        self.sub2togg.set(1)


        # y-axes tab
        self.elbl = tk.Label(self.tabAxes, text="Efficiency Graph Y-Ticks:")
        self.elbl.grid(row=0, column=0, padx=(5,5), sticky="w", columnspan=2)

        self.etext = tk.StringVar(self)
        self.ee = tk.Entry(self.tabAxes, textvariable=self.etext)
        self.ee.config(width=15)
        self.ee.grid(row=0, column=2, sticky="w", padx=(0, 5), pady="5", columnspan=3)

         # input area to designate maximum value on y2 axis
        self.y2max_label = tk.Label(self.tabAxes, text="Y Max:")
        self.y2max_label.grid(row=1, column=2, pady="5")
        self.ref_y2max = tk.StringVar(self)
        self.ref_y2max.set("1.2")

        self.comboy2max = tk.Entry(self.tabAxes, textvariable=self.ref_y2max)
        self.comboy2max.config(width=5)
        self.comboy2max.grid(row=1, column=3, sticky="w", padx=(0, 10), pady="5")

        # input area to designate minimum value on y2 axis
        self.y2min_label = tk.Label(self.tabAxes, text="Y Min:")
        self.y2min_label.grid(row=1, column=0, padx=(20,0), pady="5")
        self.ref_y2min = tk.StringVar(self)
        self.ref_y2min.set("0")

        self.comboy2min = tk.Entry(self.tabAxes, textvariable=self.ref_y2min)
        self.comboy2min.config(width=5)
        self.comboy2min.grid(row=1, column=1, sticky="w", padx=(0, 10), pady="5")


    # parses the files into a series of pandas dataframes
    def get_data(self):
        self.all_data = []
        for file in self.files:
            trajectory = open(file, "r")
            if ".csv" in self.type:
                data = pd.read_csv(trajectory)
            else:
                data = pd.read_fwf(trajectory, header=None)
                data.columns = ["time", "donor", "acceptor", "efret"]
            self.all_data.append(data)

    # creates the trajectories and pastes them into the window
    def maketrajectory(self, event=None):

        # set up variables from last generation
        if self.generation != 0:
            self.updateZero()
        self.generation += 1
        if self.trajectory is not None:
            self.trajectory.destroy()

        # parse incoming data
        self.get_data()

        # typechecking for parameters
        y2max = self.checkMinMax(self.ref_y2max.get())
        y2min = self.checkMinMax(self.ref_y2min.get())

        xfontsize = float(self.ref_xfontsize.get())
        yfontsize = float(self.ref_yfontsize.get())
        x2fontsize = float(self.ref_x2fontsize.get())
        y2fontsize = float(self.ref_y2fontsize.get())
        titlefontsize = float(self.ref_titlefontsize.get())

        # generate subtitles
        subtitles = []
        subtitlesizes = []
        for subtitle in self.subtitle_inputs:
            j, jtext, jfontsize = subtitle
            subtitles.append(j.get())
            subtitlesizes.append(jfontsize.get())
        
        yaxes = []
        ymaxes = []
        ymins = []
        for axis in self.yaxis_inputs:
            ii, itext, imax, imin = axis
            yaxes.append(ii.get())
            ymaxes.append(imax.get())
            ymins.append(imin.get())

        xmaxes = []
        xmins = []
        for axis in self.xaxis_inputs:
            xmax, xmin = axis
            xmaxes.append(xmax.get())
            xmins.append(xmin.get())

        etext = self.ee.get()
        if etext != "":
            etext = etext.strip()
            etext = etext.strip(",")
            etext = etext.strip()
            etext = etext.split(",")
            temp = []
            for val in etext:
                val = float(val)
                val = round(val, 1)
                temp.append(val)
            etext = temp
        # generate trajectory
        self.trajectory = StackedTrajectoryMaker(self.all_data, self.subframeleft, self.figtitle, self.files, self.ref_color1.get(), 
                                          self.ref_color2.get(), self.ref_color3.get(), self.ref_title.get(), titlefontsize,
                                          self.ref_x.get(), xfontsize, self.ref_x2.get(), x2fontsize, self.ref_y.get(), yfontsize, self.ref_y2.get(),
                                          y2fontsize, float(self.ref_height.get()), float(self.ref_width.get()), xmaxes, xmins, 
                                          y2max, y2min, self.intensitytogg.get(), self.efficiencytogg.get(), self.legendtogg.get(),
                                          self.subtogg.get(), self.sub2togg.get(), self.yshift, self.eyshift,
                                          self.sub3togg.get(), subtitles, subtitlesizes, self.ref_linesize.get(), self.ref_linesize2.get(), 
                                          self.ref_linesize3.get(), yaxes, ymaxes, ymins, etext)
        
        # update stored variables
        self.subtitle_length = self.trajectory.get_height()
        self.subtitles = self.trajectory.get_subtitles()
        self.subtitlesizes = self.trajectory.get_subtitlesizes()
        self.yaxisticks = self.trajectory.get_yticks()
        self.ymaxes = self.trajectory.get_ymaxes()
        self.ymins = self.trajectory.get_ymins()
        self.xmaxes = self.trajectory.get_xmaxes()
        self.xmins = self.trajectory.get_xmins()

        y2min, y2max, y2ticks = self.trajectory.getMinMax()
        self.ref_y2min.set(y2min)
        self.ref_y2max.set(y2max)
        etext = y2ticks
        temp = ""
        for val in etext:
            val = str(val)
            temp += val
            temp += ", "
        temp = temp.strip()
        temp = temp.strip(",")
        self.etext.set(temp)

        # make input areas for subtitles based on hist size
        if self.generation == 1:
            self.makeSubtitleInputs()
            for i in range(len(self.subtitle_inputs)):
                j, jtext, jfontsize = self.subtitle_inputs[i]
                f = self.files[i].split("/")[-1]
                jtext.set(f.split(".")[0])
            self.yaxisticks = self.yaxisticks[::-1]
            self.ymaxes = self.ymaxes[::-1]
            self.ymins = self.ymins[::-1]
            self.makeYAxes()
            self.makeXAxes()

        # reset subtitle input sizes
        if len(self.subtitle_inputs) == len(self.subtitles):
            for i in range(len(self.subtitle_inputs)):
                j, jtext, jfontsize = self.subtitle_inputs[i]
                jtext.set(self.subtitles[i])
                jfontsize.set(self.subtitlesizes[i])
        
        self.resetYAxes()
        self.resetXAxes()
    
    def makeYAxes(self):
        self.makeYAxisInputs()
        for i in range(len(self.yaxis_inputs)):
            ii, itext, imax, imin = self.yaxis_inputs[i]
            itext.set(self.yaxisticks[i])
            imax.set(self.ymaxes[i])
            imin.set(self.ymins[i])

    def makeXAxes(self):
        self.makeXAxisInputs()
        for i in range(len(self.xaxis_inputs)):
            xmax, xmin = self.xaxis_inputs[i]
            xmax.set(self.xmaxes[i])
            xmin.set(self.xmins[i])

    
    def makeYAxisInputs(self):
        self.yaxis_inputs = []
        k = tk.Label(self.tabAxes,text="Intensity Graph Y-Ticks: ")
        k.grid(row=2, column=0, sticky="w", padx=(5,0), pady="5", columnspan=2)
        for i in range(self.subtitle_length):
            l = tk.Label(self.tabAxes, text=f"{i+1}: ")
            l.grid(row=(2*i) + 3, column=0, padx=(20,0), sticky="w")

            itext = tk.StringVar(self)
            ii = tk.Entry(self.tabAxes, textvariable=itext)
            ii.config(width=27)
            ii.grid(row=(2*i)+3, column=1, sticky="w", padx=(0, 5), pady="5", columnspan=3)

            # input area to designate minimum value on y axis
            ymin_label = tk.Label(self.tabAxes, text="Y Min:")
            ymin_label.grid(row=(2*i)+4, column=0)
            imin = tk.StringVar(self)
            imin.set('None')

            comboymin = tk.Entry(self.tabAxes, textvariable=imin)
            comboymin.config(width=5)
            comboymin.grid(row=(2*i)+4, column=1, sticky="w", padx=(0, 0), pady="5")
            
            # input area to designate maximum value on y axis
            ymax_label = tk.Label(self.tabAxes, text="Y Max:")
            ymax_label.grid(row=(2*i)+4, column=2)
            imax = tk.StringVar(self)
            imax.set('None')

            comboymax = tk.Entry(self.tabAxes, textvariable=imax)
            comboymax.config(width=5)
            comboymax.grid(row=(2*i)+4, column=3, sticky="w", padx=(0, 0), pady="5")

            self.yaxis_inputs.append((ii, itext, imax, imin))

    def makeXAxisInputs(self):
        self.xaxis_inputs = []
        k = tk.Label(self.tabFormat,text="X-Axes:")
        k.grid(row=6, column=0, sticky="w", padx=(5,0), pady="5", columnspan=2)
        for i in range(self.subtitle_length):
            # input area to designate minimum value on y axis
            xmin_label = tk.Label(self.tabFormat, text=f"({i+1}) X Min:")
            xmin_label.grid(row=(i+6), column=0, padx=(5,5))
            xmin = tk.StringVar(self)
            xmin.set('None')

            comboxmin = tk.Entry(self.tabFormat, textvariable=xmin)
            comboxmin.config(width=8)
            comboxmin.grid(row=(i+6), column=1, sticky="w", padx=(0, 0), pady="5")
            
            # input area to designate maximum value on y axis
            xmax_label = tk.Label(self.tabFormat, text="X Max:")
            xmax_label.grid(row=(i+6), column=2, padx=(5,5))
            xmax = tk.StringVar(self)
            xmax.set('None')

            comboxmax = tk.Entry(self.tabFormat, textvariable=xmax)
            comboxmax.config(width=8)
            comboxmax.grid(row=(i+6), column=3, sticky="w", padx=(0, 0), pady="5")

            self.xaxis_inputs.append((xmax, xmin))

    # reset subtitle input sizes
    def resetYAxes(self):
        if len(self.yaxis_inputs) == len(self.yaxisticks):
            for i in range(len(self.yaxis_inputs)):
                ii, itext, imax, imin = self.yaxis_inputs[i]
                itext.set(self.yaxisticks[i])
                imax.set(self.ymaxes[i])
                imin.set(self.ymins[i])

                temp = itext.get()
                temp = temp.strip("[]")
                temp = temp.strip("()")
                temp = temp.strip()
                temp = temp.strip(".")
                itext.set(temp)
    
    # reset subtitle input sizes
    def resetXAxes(self):
        if len(self.xaxis_inputs) == len(self.xmins):
            for i in range(len(self.xaxis_inputs)):
                xmax, xmin = self.xaxis_inputs[i]
                xmax.set(self.xmaxes[i])
                xmin.set(self.xmins[i])


    # creates input areas and fontsize dropdowns based on length of data provided to histogram
    def makeSubtitleInputs(self):
        self.subtitle_inputs = []
        k = tk.Label(self.tabSub,text="Plot Subtitles: ")
        k.grid(row=0, column=0, columnspan=2)
        for i in range(self.subtitle_length):
            l = tk.Label(self.tabSub, text=f"{i+1}: ")
            l.grid(row=i + 1, column=0, padx=(10,5))

            jtext = tk.StringVar(self)
            j = tk.Entry(self.tabSub, textvariable=jtext)
            j.config(width=20)
            j.grid(row=i+1, column=1, sticky="ew", padx=(0, 10))

            jfont = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
            jvar = tk.IntVar(self)
            jvar.set(10)
            jfontwidget = tk.OptionMenu(self.tabSub, jvar, *jfont)
            jfontwidget.grid(row=i+1, column=2)
            jfontwidget.config(width=2)

            self.subtitle_inputs.append((j, jtext, jvar))

    # type checks the designation of x/y mins and maxes
    # - val: value input into x/y min or max entry boxes
    def checkMinMax(self, val):
        if val != 'None':
            val = float(val)
        else:
            val = None
        return val
    
    # creates a small window for user to enter the path to save the trajectories to
    # only needs to be set once, defaults to the same folder provided by the user
    #   when originally opening the data
    def savewindow(self):
        self.win = tk.Toplevel()
        self.win.title("Set Filepath: ")
        
        #input area for file name
        self.path_label = tk.Label(self.win, text="Save File Path:")
        self.path_label.grid(row=0, column=0)
        self.ref_path = tk.StringVar(self.win)
        self.ref_path.set(self.path)

        self.combo6 = tk.Entry(self.win, textvariable=self.ref_path)
        self.combo6.config(width=50)
        self.combo6.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady="10")

        # dropdown for designation of filetype
        reftype = ['.pdf', '.png', '.svg', '.ps', '.eps']
        self.ref_type = tk.StringVar(self)
        self.ref_type.set('.png')

        self.combo8 = tk.OptionMenu(self.win, self.ref_type, *reftype)
        self.combo8.config(width=5)
        self.combo8.grid(row=0, column=2, sticky="ew", padx=(0, 10), pady="10")

        # dropdown for designation of file quality
        self.qual_label = tk.Label(self.win, text="Quality:")
        self.qual_label.grid(row= 1, column=0)
        refqual = ["Low", "Medium", "High"]
        self.ref_qual = tk.StringVar(self)
        self.ref_qual.set('High')

        self.combo9 = tk.OptionMenu(self.win, self.ref_qual, *refqual)
        self.combo9.config(width=5)
        self.combo9.grid(row=1, column=1, sticky="w", padx=(0, 10), pady="10")

        # save button
        self.saveButton = tk.Button(self.win, text="SAVE", command=self.save)
        self.saveButton.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)

    # save trajectory to designated file path at given type & quality  
    def save(self):
        self.trajectory.save(self.ref_path.get(), self.ref_type.get(), self.ref_qual.get())
        self.win.destroy()
    
    # opens native color chooser dialog
    def choose_plotAcolor(self):
        color_code, hexcode = colorchooser.askcolor(title="Choose Color")
        self.ref_color1.set(hexcode)

    # opens native color chooser dialog
    def choose_plotBcolor(self):
        color_code, hexcode = colorchooser.askcolor(title="Choose Color")
        self.ref_color2.set(hexcode)

     # opens native color chooser dialog
    def choose_plotCcolor(self):
        color_code, hexcode = colorchooser.askcolor(title="Choose Color")
        self.ref_color3.set(hexcode)
    
    # get shift data from trajectory
    # to be carried over to the next trajectory generation  
    def updateZero(self, event=None):
        self.yshift, self.eyshift = self.trajectory.getShift()
    
    # if click-to-zero is active, will set the zeroing to none
    # so displayed data is un-modified
    def undo(self, event=None):
        if self.sub3togg.get() == 1:
            self.trajectory.setShift(0.0, 0.0)
            self.maketrajectory()