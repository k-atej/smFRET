from tkinter import colorchooser, ttk
import pandas as pd
import tkinter as tk
from fileviewer.fileViewerMaker import *

#TO DO: remove plot customizability options and side window


class FileViewerWindow(tk.Toplevel):
    def __init__(self, path, files):
        super().__init__()
        self.minsize(200, 200)
        self.df = []
        self.files = [] # name of final file
        for file in files:
            self.files.append(file.split("/")[-1])
        self.paths = files # full file path
        self.numfiles = len(self.paths)
        self.index = 0
        self.trajectory = None

        self.savepath = path.rstrip("/")
        print(self.savepath)
        
        self.titleset = path.split("/")[-1] # final folder in the input path
        self.title(self.titleset)
        self.yshift = 0
        self.generation = 0

        self.dwellActive = False
        self.dwelltimedf = pd.DataFrame(columns=['Series', 'deltaT'])
        self.dwellseries = 0

        self.filepath = self.savepath
        self.type = '.csv'

        #full window 
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)

        #area above the intensity viewer
        self.subframetop = tk.Frame(self.frame, background='white')
        self.subframetop.grid(row=0, column=0, columnspan=2)

        # left half (contains intensities and efret figures)
        self.subframeleft = tk.Frame(self.frame, background='white')
        self.subframeleft.grid(row=1, column=0, padx=(20, 0))

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

    def start(self):
        #self.makeFormat() #not visible, for now
        self.makeButtons()
        #self.makeOptions()
        self.maketrajectory()
        #self.bind('<Return>', self.maketrajectory)
        self.bind('<BackSpace>', self.undo)
        self.bind('<Left>', self.back)
        self.bind('<Right>', self.next1)
        self.bind('<Return>', self.save)

        
    
    def makeButtons(self):
        # generate button, bound to the generation of a histogram
        makeTraj = tk.Button(self.subframetop, text="Regenerate", command=self.maketrajectory)
        makeTraj.grid(row=0, column=7, padx="10")

        # back button
        self.backbutton = tk.Button(self.subframetop, text="Back", command=self.back)
        self.backbutton.grid(row=0, column=1, padx="10")

        # next button
        self.nextbutton = tk.Button(self.subframetop, text="Next", command=self.next1)
        self.nextbutton.grid(row=0, column=2, padx="10", pady="10")
    
        # save button
        self.saveButton = tk.Button(self.subframetop, text="Set Filepath", command=self.savewindow)
        self.saveButton.grid(row=0, column=3, sticky="ew", padx="10", pady="10")

        # click-to-zero toggle
        self.sub3togg = tk.IntVar()
        self.togglesub3 = tk.Checkbutton(self.subframetop, text="Click to Zero", variable=self.sub3togg, onvalue=1, offvalue=0)
        self.togglesub3.grid(row=0, column=4, sticky="ew", padx="10", pady="10")
        self.sub3togg.set(0)

        # sum toggle
        self.sumtogg = tk.IntVar()
        self.togglesum = tk.Checkbutton(self.subframetop, text="Show Sum", variable=self.sumtogg, onvalue=1, offvalue=0)
        self.togglesum.grid(row=0, column=6, sticky="ew", padx="10", pady="10")
        self.sumtogg.set(0)

        # dwell time analysis button
        self.dwellButton = tk.Button(self.subframetop, text="Show Dwell Time Analysis", command=self.dwellClicks)
        self.dwellButton.grid(row=0, column=8, sticky="ew", padx="10", pady="10")
        self.dwelltogg = tk.IntVar()
        self.dwelltogg.set(0)


    def dwellClicks(self):
        if self.dwellActive == False:
            self.updateDwellTable()
        else:
            self.tree = None
            for widget in self.subframeright.winfo_children():
                widget.destroy()
            self.dwellActive = False
            self.maketrajectory()

    def updateDwellTable(self, event=None):
        self.sub3togg.set(0)
        self.original_size = (self.winfo_width(), self.winfo_height())
        self.tree = ttk.Treeview(self.subframeright, show="headings")

        self.tree["columns"] = list(self.dwelltimedf.columns)
        self.tree.column("Series", anchor="center", width=50, stretch=False)
        self.tree.heading("Series", text="Series")
        self.tree.column("deltaT", anchor="center", width=250, stretch=False)
        self.tree.heading("deltaT", text="deltaT")

        for index, row in self.dwelltimedf.iterrows():
            self.tree.insert("", "end", values=list(row))

        # dwell time selection toggle
        self.toggledwell = tk.Checkbutton(self.subframeright, text="Click to Select Dwell Times", variable=self.dwelltogg, onvalue=1, offvalue=0)
        self.toggledwell.grid(row=0, column=0, padx=(10, 20), pady="10", columnspan=3)

        self.tree.grid(row=1, column=0, sticky="ew", padx=(10, 20), pady="10", columnspan=3)
        self.refreshButton = tk.Button(self.subframeright, text="Refresh", command=self.updateDwellTable)
        self.refreshButton.grid(row=2, column=0, sticky="ew", padx=(10,20), pady="10")

        self.seriesButton = tk.Button(self.subframeright, text="+ Series", command=self.addSeries)
        self.seriesButton.grid(row=2, column=1, sticky="ew", padx=(10,20), pady="10")

        self.seriesSaveButton = tk.Button(self.subframeright, text="Save", command=self.saveSeries)
        self.seriesSaveButton.grid(row=2, column=2, sticky="ew", padx=(10,20), pady="10")

        self.dwellActive = True
        self.dwellseries = self.trajectory.getDwellSeries()
        self.maketrajectory()

    def addSeries(self):
        self.trajectory.incrementDwellSeries()


    def makeFormat(self):
        self.tabControl = ttk.Notebook(master=self.subframerighttop)
        self.tabFormat = tk.Frame(self.tabControl)
        self.tabControl.grid(row=0, column=0, rowspan=2, padx=10, sticky='n')

        self.tabFormat = tk.Frame(self.tabControl)
        self.tabStyle = tk.Frame(self.tabControl)
        self.tabText = tk.Frame(self.tabControl)

        self.tabControl.add(self.tabFormat, text="Format")
        self.tabControl.add(self.tabStyle, text="Style")
        self.tabControl.add(self.tabText, text="Text")



    def makeOptions(self):
        # tab 1: format
         # input area to designate maximum value on x axis
        #check box for toggling to bin width input
        self.intensitytogg = tk.IntVar()
        self.toggle1 = tk.Checkbutton(self.tabFormat, text="Intensity Plot", variable=self.intensitytogg, onvalue=1, offvalue=0)
        self.toggle1.grid(row=3, column=0, sticky="ew", padx=(10,10), pady=(10,5), columnspan=2)
        self.intensitytogg.set(1)

        self.efficiencytogg = tk.IntVar()
        self.toggle2 = tk.Checkbutton(self.tabFormat, text="Efficiency Plot", variable=self.efficiencytogg, onvalue=1, offvalue=0)
        self.toggle2.grid(row=6, column=0, sticky="ew", padx=(10,10), pady=(10,5), columnspan=2)
        self.efficiencytogg.set(1)

        self.xmax_label = tk.Label(self.tabFormat, text="X Max:")
        self.xmax_label.grid(row=4, column=2, pady="5")
        self.ref_xmax = tk.StringVar(self)
        self.ref_xmax.set("None")

        self.comboxmax = tk.Entry(self.tabFormat, textvariable=self.ref_xmax)
        self.comboxmax.config(width=5)
        self.comboxmax.grid(row=4, column=3, sticky="ew", padx=(0, 10), pady="5")

        # input area to designate minimum value on x axis
        self.xmin_label = tk.Label(self.tabFormat, text="X Min:")
        self.xmin_label.grid(row=4, column=0, padx=(20,0), pady="5")
        self.ref_xmin = tk.StringVar(self)
        self.ref_xmin.set("0")

        self.comboxmin = tk.Entry(self.tabFormat, textvariable=self.ref_xmin)
        self.comboxmin.config(width=5)
        self.comboxmin.grid(row=4, column=1, sticky="ew", padx=(0, 10), pady="5")

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
        self.ref_ymin.set("None")

        self.comboymin = tk.Entry(self.tabFormat, textvariable=self.ref_ymin)
        self.comboymin.config(width=5)
        self.comboymin.grid(row=5, column=1, sticky="ew", padx=(0, 10), pady="5")

        # input area to designate maximum value on y2 axis
        self.y2max_label = tk.Label(self.tabFormat, text="Y Max:")
        self.y2max_label.grid(row=7, column=2, pady="5")
        self.ref_y2max = tk.StringVar(self)
        self.ref_y2max.set("1.2")

        self.comboy2max = tk.Entry(self.tabFormat, textvariable=self.ref_y2max)
        self.comboy2max.config(width=5)
        self.comboy2max.grid(row=7, column=3, sticky="ew", padx=(0, 10), pady="5")

        # input area to designate minimum value on y2 axis
        self.y2min_label = tk.Label(self.tabFormat, text="Y Min:")
        self.y2min_label.grid(row=7, column=0, padx=(20,0), pady="5")
        self.ref_y2min = tk.StringVar(self)
        self.ref_y2min.set("None")

        self.comboy2min = tk.Entry(self.tabFormat, textvariable=self.ref_y2min)
        self.comboy2min.config(width=5)
        self.comboy2min.grid(row=7, column=1, sticky="ew", padx=(0, 10), pady="5")

        self.fig_label = tk.Label(self.tabFormat, text="Figure Dimensions")
        self.fig_label.grid(row=0, column=0, columnspan=2, pady=(10,5))


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

        self.e_label = tk.Label(self.tabStyle, text="Efficiency Plot:")
        self.e_label.grid(row=4, column=0, columnspan=2, pady=(10,5), sticky="w")

        # input area for designation of plot3 color
        self.color_label = tk.Label(self.tabStyle, text="Efficiency:")
        self.color_label.grid(row=5, column=0, padx=(20,0))
        self.ref_color3 = tk.StringVar(self)
        self.ref_color3.set("black")

        self.combo4 = tk.Entry(self.tabStyle, textvariable=self.ref_color3)
        self.combo4.config(width=5)
        self.combo4.grid(row=5, column=1, sticky="ew", padx=(0, 10), pady="5")

        # color wheel for designation of plot3 color
        self.color2button = tk.Button(self.tabStyle, text="Select Color", command=self.choose_plotCcolor)
        self.color2button.grid(row=5, column=3)


        # third tab: text
        # all of these should be toggled on & off with each subplot, should toggle overall title individually

        # input area for designation of graph title
        self.title_label = tk.Label(self.tabText, text="Title:")
        self.title_label.grid(row=0, column=0)
        self.ref_title = tk.StringVar(self)
        self.ref_title.set(self.titleset)

        self.combo2 = tk.Entry(self.tabText, textvariable=self.ref_title)
        self.combo2.config(width=10)
        self.combo2.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady="5")

        # dropdown for title font size
        self.titlef_label = tk.Label(self.tabText, text="Size:")
        self.titlef_label.grid(row=0, column=2)
        titlef = [8, 9, 10, 11, 12, 15, 20, 24]
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
        self.ref_y2.set("E")

        self.combo3 = tk.Entry(self.tabText, textvariable=self.ref_y2)
        self.combo3.config(width=10)
        self.combo3.grid(row=7, column=1, sticky="ew", padx=(0, 10), pady="5")

        # dropdown for x font size
        self.titlex_label = tk.Label(self.tabText, text="Size:")
        self.titlex_label.grid(row=2, column=2)
        titlex = [8, 9, 10, 11, 12, 15, 20, 24]
        self.ref_xfontsize = tk.StringVar(self)
        self.ref_xfontsize.set("12")

        self.combo4 = tk.OptionMenu(self.tabText, self.ref_xfontsize, *titlex)
        self.combo4.config(width=1)
        self.combo4.grid(row=2, column=3)

        # dropdown for y font size
        self.titley_label = tk.Label(self.tabText, text="Size:")
        self.titley_label.grid(row=3, column=2)
        titley = [8, 9, 10, 11, 12, 15, 20, 24]
        self.ref_yfontsize = tk.StringVar(self)
        self.ref_yfontsize.set("12")

        self.combo = tk.OptionMenu(self.tabText, self.ref_yfontsize, *titley)
        self.combo.config(width=1)
        self.combo.grid(row=3, column=3)

        # dropdown for x2 font size
        self.titlex2_label = tk.Label(self.tabText, text="Size:")
        self.titlex2_label.grid(row=6, column=2)
        titlex2 = [8, 9, 10, 11, 12, 15, 20, 24]
        self.ref_x2fontsize = tk.StringVar(self)
        self.ref_x2fontsize.set("12")

        self.combo4 = tk.OptionMenu(self.tabText, self.ref_x2fontsize, *titlex2)
        self.combo4.config(width=1)
        self.combo4.grid(row=6, column=3)

        # dropdown for y2 font size
        self.titley2_label = tk.Label(self.tabText, text="Size:")
        self.titley2_label.grid(row=7, column=2)
        titley2 = [8, 9, 10, 11, 12, 15, 20, 24]
        self.ref_y2fontsize = tk.StringVar(self)
        self.ref_y2fontsize.set("12")

        self.combo = tk.OptionMenu(self.tabText, self.ref_y2fontsize, *titley2)
        self.combo.config(width=1)
        self.combo.grid(row=7, column=3)

        # subtitle toggle: intensity
        self.subtogg = tk.IntVar()
        self.togglesub = tk.Checkbutton(self.tabText, text="Subtitle", variable=self.subtogg, onvalue=1, offvalue=0)
        self.togglesub.grid(row=4, column=0, sticky="ew", padx=(15,10), pady="5", columnspan=2)
        self.subtogg.set(1)

        # subtitle toggle: efficiency
        self.sub2togg = tk.IntVar()
        self.togglesub2 = tk.Checkbutton(self.tabText, text="Subtitle", variable=self.sub2togg, onvalue=1, offvalue=0)
        self.togglesub2.grid(row=8, column=0, sticky="ew", padx=(15,10), pady="5", columnspan=2)
        self.sub2togg.set(1)

    # parses the data file into a pandas dataframe
    def get_data(self):
        trajectories = open(self.paths[self.index], "r") 
        data = pd.read_fwf(trajectories, header=None)
        data.columns = ["time", "donor", "acceptor"]
        self.df = data


    def maketrajectory(self, event=None):
        if self.generation != 0:
            self.updateZero()
        self.generation += 1
        
        if self.trajectory is not None:
            self.trajectory.destroyWidget()
        self.get_data()

        title = self.paths[self.index]
        xfontsize = 12.0
        yfontsize = 12.0
        x2fontsize = 12.0
        y2fontsize = 12.0
        titlefontsize = 12.0

        summ = self.sumtogg.get() # on = 1


        self.trajectory = FileViewerMaker(title, self.titleset, self.df, self.subframeleft, "lime", 
                                          "red", "black", self.titleset, titlefontsize,
                                          "Time (s)", xfontsize, "Time (s)", x2fontsize, " ", yfontsize, 
                                          " ", y2fontsize, 4.5, 6.0, None, None, None, 
                                          None, None, None, 1, 1, 0,
                                          1, 1, self.yshift, self.sub3togg.get(), summ, 
                                          self.dwelltogg.get(), self.dwelltimedf, self.dwellseries)

        self.dwelltimedf = self.trajectory.getDwellData()
        self.dwellseries = self.trajectory.getDwellSeries()
        self.makeLabel()

    # type checks the designation of x/y mins and maxes
    # - val: value input into x/y min or max entry boxes
    def checkMinMax(self, val):
        if val != 'None':
            val = float(val)
        else:
            val = None
        return val

    def back(self, event=None):
        self.index -= 1
        if self.index < 0:
            self.index = self.numfiles - 1
        self.trajectory.setShift(0.0)
        self.maketrajectory()


    def next1(self, event=None):
        self.index += 1
        if self.index >= self.numfiles:
            self.index = 0
        self.trajectory.setShift(0.0)
        self.maketrajectory()

    def makeLabel(self):
        self.label = tk.Label(self.subframetop, text=f"{self.index + 1} of {self.numfiles}")    
        self.label.grid(row=0, column=0, padx="10")

    def savewindow(self):
        self.win = tk.Toplevel()
        self.win.title("Set Filepath: ")
        self.unbind_all('<Return>')
        self.win.bind('<Return>', self.setfilepath)
        
        #input area for file name
        self.path_label = tk.Label(self.win, text="Save Filepath:")
        self.path_label.grid(row=0, column=0)
        self.ref_path = tk.StringVar(self.win)
        self.ref_path.set(self.filepath)

        self.combo6 = tk.Entry(self.win, textvariable=self.ref_path)
        self.combo6.config(width=50)
        self.combo6.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady="10")

        # dropdown for designation of filetype

        self.type_label = tk.Label(self.win, text="Save Data Files As:")
        self.type_label.grid(row=1, column=0)
        reftype = ['.csv']

        self.ref_type = tk.StringVar(self)
        self.ref_type.set('.csv')
        self.combo8 = tk.OptionMenu(self.win, self.ref_type, *reftype)
        self.combo8.config(width=5)
        self.combo8.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="10")

        # dropdown for designation of file quality
        #self.qual_label = tk.Label(self.win, text="Quality:")
        #self.qual_label.grid(row= 1, column=0)
        #refqual = ["Low", "Medium", "High"]
        
        #self.ref_qual = tk.StringVar(self)
        #self.ref_qual.set('Medium')

        #self.combo9 = tk.OptionMenu(self.win, self.ref_qual, *refqual)
        #self.combo9.config(width=5)
        #self.combo9.grid(row=1, column=1, sticky="w", padx=(0, 10), pady="10")


        self.saveButton = tk.Button(self.win, text="SAVE", command=self.setfilepath)
        self.saveButton.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)
        
        #self.win.mainloop()
    
    def setfilepath(self, event=None):
        self.filepath = self.ref_path.get()
        self.type = self.ref_type.get()
        self.win.destroy()
        self.win.unbind_all('<Return>')
        self.bind('<Return>', self.save)
        
    
    def save(self, event=None):
        self.trajectory.save(self.filepath, self.type) # modify this to set filepath
        self.next1()

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

    def updateZero(self, event=None):
        self.yshift = self.trajectory.getShift()

    def undo(self, event=None):
        if self.sub3togg.get() == 1:
            self.trajectory.setShift(0.0)
            self.trajectory.destroyWidget()
            self.maketrajectory()

    def saveSeries(self):
        self.win = tk.Toplevel()
        self.win.title("Save Dwell Time Data: ")
        self.unbind_all('<Return>')
        self.win.bind('<Return>', self.saveSeriesData)
        
        #input area for file name
        self.path_label = tk.Label(self.win, text="Save Filepath:")
        self.path_label.grid(row=0, column=0)
        self.ref_path = tk.StringVar(self.win)
        self.ref_path.set(self.filepath)

        self.combo6 = tk.Entry(self.win, textvariable=self.ref_path)
        self.combo6.config(width=50)
        self.combo6.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady="10")

        # dropdown for designation of filetype

        self.type_label = tk.Label(self.win, text="Save File As:")
        self.type_label.grid(row=1, column=0)
        reftype = ['.csv']

        self.ref_type = tk.StringVar(self)
        self.ref_type.set('.csv')
        self.combo8 = tk.OptionMenu(self.win, self.ref_type, *reftype)
        self.combo8.config(width=5)
        self.combo8.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="10")

        self.saveButton = tk.Button(self.win, text="SAVE", command=self.saveSeriesData)
        self.saveButton.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)

    
    def saveSeriesData(self, event=None):
        self.filepath = self.ref_path.get()
        self.type = self.ref_type.get()
        self.trajectory.saveDwellData(self.filepath, self.type)
        self.win.destroy()
        self.win.unbind_all('<Return>')
        self.bind('<Return>', self.save)