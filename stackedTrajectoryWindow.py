import pandas as pd
import tkinter as tk
from histogramMaker import *
from histogramWindow import *
from stackedHistogramWindow import *
from trajectoryMaker import *
from stackedTrajectoryMaker import *



class stackedTrajectoryWindow(tk.Toplevel):
    def __init__(self, path, files):
        super().__init__()
        self.minsize(200, 200)
        self.path = path  # what the user input into the box in the menu
        self.files = files  # list of filepaths for every trace file found within the folder
        self.figtitle = self.path.split("/")[-1]
        self.title(self.figtitle)
        self.trajectory = None

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

    def start(self):
        self.makeFormat()
        self.makeButtons()
        self.makeOptions() 
        self.maketrajectory()
        self.bind('<Return>', self.maketrajectory)


    def makeButtons(self):
        # generate button, bound to the generation of a histogram
        makeTraj = tk.Button(self.subframetop, text="Generate", command=self.maketrajectory)
        makeTraj.grid(row=0, column=0, padx="10")

        # save button
        self.saveButton = tk.Button(self.subframetop, text="Save", command=self.savewindow)
        self.saveButton.grid(row=0, column=1, sticky="ew", padx="10", pady="10")
    
    
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

        self.tabControl2 = ttk.Notebook(master=self.subframerightbottom)
        self.tabFormat2 = tk.Frame(self.tabControl2)
        self.tabControl2.grid(row=0, column=0, rowspan=2, padx=10, sticky='n')

        self.tabFormat2 = tk.Frame(self.tabControl2)
        self.tabStyle2 = tk.Frame(self.tabControl2)
        self.tabText2 = tk.Frame(self.tabControl2)

        self.tabControl2.add(self.tabFormat2, text="Format")
        self.tabControl2.add(self.tabStyle2, text="Style")
        self.tabControl2.add(self.tabText2, text="Text")

    def makeOptions(self):
        # tab 1: format

        self.xmax_label = tk.Label(self.tabFormat, text="X Max:")
        self.xmax_label.grid(row=0, column=2)
        self.ref_xmax = tk.StringVar(self)
        self.ref_xmax.set("None")

        self.comboxmax = tk.Entry(self.tabFormat, textvariable=self.ref_xmax)
        self.comboxmax.config(width=5)
        self.comboxmax.grid(row=0, column=3, sticky="ew", padx=(0, 0), pady="10")

        # input area to designate minimum value on x axis
        self.xmin_label = tk.Label(self.tabFormat, text="X Min:")
        self.xmin_label.grid(row=0, column=0)
        self.ref_xmin = tk.StringVar(self)
        self.ref_xmin.set("0")

        self.comboxmin = tk.Entry(self.tabFormat, textvariable=self.ref_xmin)
        self.comboxmin.config(width=5)
        self.comboxmin.grid(row=0, column=1, sticky="ew", padx=(0, 0), pady="10")

        # input area to designate maximum value on y axis
        self.ymax_label = tk.Label(self.tabFormat, text="Y Max:")
        self.ymax_label.grid(row=1, column=2)
        self.ref_ymax = tk.StringVar(self)
        self.ref_ymax.set("None")

        self.comboymax = tk.Entry(self.tabFormat, textvariable=self.ref_ymax)
        self.comboymax.config(width=5)
        self.comboymax.grid(row=1, column=3, sticky="ew", padx=(0, 10), pady="10")

        # input area to designate minimum value on y axis
        self.ymin_label = tk.Label(self.tabFormat, text="Y Min:")
        self.ymin_label.grid(row=1, column=0)
        self.ref_ymin = tk.StringVar(self)
        self.ref_ymin.set("0")

        self.comboymin = tk.Entry(self.tabFormat, textvariable=self.ref_ymin)
        self.comboymin.config(width=5)
        self.comboymin.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="10")

        # input area to designate maximum value on y2 axis
        self.y2max_label = tk.Label(self.tabFormat2, text="Y Max 2:")
        self.y2max_label.grid(row=2, column=2)
        self.ref_y2max = tk.StringVar(self)
        self.ref_y2max.set("1.2")

        self.comboy2max = tk.Entry(self.tabFormat2, textvariable=self.ref_y2max)
        self.comboy2max.config(width=5)
        self.comboy2max.grid(row=2, column=3, sticky="ew", padx=(0, 10), pady="10")

        # input area to designate minimum value on y2 axis
        self.y2min_label = tk.Label(self.tabFormat2, text="Y Min 2:")
        self.y2min_label.grid(row=2, column=0)
        self.ref_y2min = tk.StringVar(self)
        self.ref_y2min.set("0")

        self.comboy2min = tk.Entry(self.tabFormat2, textvariable=self.ref_y2min)
        self.comboy2min.config(width=5)
        self.comboy2min.grid(row=2, column=1, sticky="ew", padx=(0, 10), pady="10")

        # input area for figure width
        self.width_label = tk.Label(self.tabFormat, text="Width:")
        self.width_label.grid(row=3, column=0)
        self.ref_width = tk.StringVar(self)
        self.ref_width.set('7')

        self.combowidth = tk.Entry(self.tabFormat, textvariable=self.ref_width)
        self.combowidth.config(width=5)
        self.combowidth.grid(row=3, column=1, sticky="ew", padx=(0, 10), pady="10")

         # input area for figure height
        self.height_label = tk.Label(self.tabFormat, text="Height:")
        self.height_label.grid(row=3, column=2)
        self.ref_height = tk.StringVar(self)
        self.ref_height.set('5.5')

        self.comboheight = tk.Entry(self.tabFormat, textvariable=self.ref_height)
        self.comboheight.config(width=5)
        self.comboheight.grid(row=3, column=3, sticky="ew", padx=(0, 10), pady="10")



        # tab2 : style

         # input area for designation of plot1 color
        self.color_label = tk.Label(self.tabStyle, text="Color A:")
        self.color_label.grid(row=0, column=0)
        self.ref_color1 = tk.StringVar(self)
        self.ref_color1.set("lime")

        self.combo2 = tk.Entry(self.tabStyle, textvariable=self.ref_color1)
        self.combo2.config(width=5)
        self.combo2.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady="10")

        # color wheel for designation of plot1 color
        self.color1button = tk.Button(self.tabStyle, text="Select Color", command=self.choose_plotAcolor)
        self.color1button.grid(row=0, column=3)

        
        
        # input area for designation of plot2 color
        self.color_label = tk.Label(self.tabStyle, text="Color B:")
        self.color_label.grid(row=1, column=0)
        self.ref_color2 = tk.StringVar(self)
        self.ref_color2.set("red")

        self.combo3 = tk.Entry(self.tabStyle, textvariable=self.ref_color2)
        self.combo3.config(width=5)
        self.combo3.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="10")

        # color wheel for designation of plot2 color
        self.color2button = tk.Button(self.tabStyle, text="Select Color", command=self.choose_plotBcolor)
        self.color2button.grid(row=1, column=3)



        # input area for designation of plot3 color
        self.color_label = tk.Label(self.tabStyle2, text="Color C:")
        self.color_label.grid(row=2, column=0)
        self.ref_color3 = tk.StringVar(self)
        self.ref_color3.set("black")

        self.combo4 = tk.Entry(self.tabStyle2, textvariable=self.ref_color3)
        self.combo4.config(width=5)
        self.combo4.grid(row=2, column=1, sticky="ew", padx=(0, 10), pady="10")

        # color wheel for designation of plot3 color
        self.color2button = tk.Button(self.tabStyle2, text="Select Color", command=self.choose_plotCcolor)
        self.color2button.grid(row=2, column=3)


        # third tab: text
        # all of these should be toggled on & off with each subplot, should toggle overall title individually

        # input area for designation of graph title
        self.title_label = tk.Label(self.tabText, text="Title:")
        self.title_label.grid(row=0, column=0)
        self.ref_title = tk.StringVar(self)
        self.ref_title.set("Title")

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
        self.combo.config(width=3)
        self.combo.grid(row=0, column=3)

        # input area for designation of intensity x-axis label
        self.x_label = tk.Label(self.tabText, text="X-Axis Label 1:")
        self.x_label.grid(row=1, column=0)
        self.ref_x = tk.StringVar(self)
        self.ref_x.set("X-Axis")

        self.combo2 = tk.Entry(self.tabText, textvariable=self.ref_x)
        self.combo2.config(width=10)
        self.combo2.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="5")

        # input area for designation of efficiency x-axis label
        self.x2_label = tk.Label(self.tabText2, text="X-Axis Label 2:")
        self.x2_label.grid(row=2, column=0)
        self.ref_x2 = tk.StringVar(self)
        self.ref_x2.set("X-Axis")

        self.combo2 = tk.Entry(self.tabText2, textvariable=self.ref_x2)
        self.combo2.config(width=10)
        self.combo2.grid(row=2, column=1, sticky="ew", padx=(0, 10), pady="5")

        # input area for designation of intensity y-axis label
        self.y_label = tk.Label(self.tabText, text="Y-Axis Label 1:")
        self.y_label.grid(row=3, column=0)
        self.ref_y = tk.StringVar(self)
        self.ref_y.set("Y-Axis")

        self.combo3 = tk.Entry(self.tabText, textvariable=self.ref_y)
        self.combo3.config(width=10)
        self.combo3.grid(row=3, column=1, sticky="ew", padx=(0, 10), pady="5")

        # input area for designation of efficiency y-axis label
        self.y2_label = tk.Label(self.tabText2, text="Y-Axis Label 2:")
        self.y2_label.grid(row=4, column=0)
        self.ref_y2 = tk.StringVar(self)
        self.ref_y2.set("Y-Axis")

        self.combo3 = tk.Entry(self.tabText2, textvariable=self.ref_y2)
        self.combo3.config(width=10)
        self.combo3.grid(row=4, column=1, sticky="ew", padx=(0, 10), pady="5")

        # dropdown for x font size
        self.titlex_label = tk.Label(self.tabText, text="Size:")
        self.titlex_label.grid(row=1, column=2)
        titlex = [8, 9, 10, 11, 12, 15, 20, 24]
        self.ref_xfontsize = tk.StringVar(self)
        self.ref_xfontsize.set("12")

        self.combo4 = tk.OptionMenu(self.tabText, self.ref_xfontsize, *titlex)
        self.combo4.config(width=3)
        self.combo4.grid(row=1, column=3)

        # dropdown for y font size
        self.titley_label = tk.Label(self.tabText, text="Size:")
        self.titley_label.grid(row=3, column=2)
        titley = [8, 9, 10, 11, 12, 15, 20, 24]
        self.ref_yfontsize = tk.StringVar(self)
        self.ref_yfontsize.set("12")

        self.combo = tk.OptionMenu(self.tabText, self.ref_yfontsize, *titley)
        self.combo.config(width=3)
        self.combo.grid(row=3, column=3)

        # dropdown for x2 font size
        self.titlex2_label = tk.Label(self.tabText2, text="Size:")
        self.titlex2_label.grid(row=2, column=2)
        titlex2 = [8, 9, 10, 11, 12, 15, 20, 24]
        self.ref_x2fontsize = tk.StringVar(self)
        self.ref_x2fontsize.set("12")

        self.combo4 = tk.OptionMenu(self.tabText2, self.ref_x2fontsize, *titlex2)
        self.combo4.config(width=3)
        self.combo4.grid(row=2, column=3)

        # dropdown for y2 font size
        self.titley2_label = tk.Label(self.tabText2, text="Size:")
        self.titley2_label.grid(row=4, column=2)
        titley2 = [8, 9, 10, 11, 12, 15, 20, 24]
        self.ref_y2fontsize = tk.StringVar(self)
        self.ref_y2fontsize.set("12")

        self.combo = tk.OptionMenu(self.tabText2, self.ref_y2fontsize, *titley2)
        self.combo.config(width=3)
        self.combo.grid(row=4, column=3)

    # HOW DO I NEED TO RESTRUCTURE THIS?

    # parses the files into a series of pandas dataframes
    def get_data(self):
        self.all_data = []
        for file in self.files:
            trajectory = open(file, "r") 
            data = pd.read_fwf(trajectory, header=None)
            data.columns = ["time", "donor", "acceptor"]
            self.all_data.append(data)

    def calculateEfret(self):
        for data in self.all_data:
            gamma = 1
            data['efret'] = data['acceptor'] / (data['acceptor'] + (gamma * data['donor']))

    def maketrajectory(self, event=None):
        if self.trajectory is not None:
            self.trajectory.destroy()
        self.get_data()
        self.calculateEfret()
        xmax = self.checkMinMax(self.ref_xmax.get())
        xmin = self.checkMinMax(self.ref_xmin.get())
        ymax = self.checkMinMax(self.ref_ymax.get())
        ymin = self.checkMinMax(self.ref_ymin.get())
        y2max = self.checkMinMax(self.ref_y2max.get())
        y2min = self.checkMinMax(self.ref_y2min.get())

        xfontsize = float(self.ref_xfontsize.get())
        yfontsize = float(self.ref_yfontsize.get())
        x2fontsize = float(self.ref_x2fontsize.get())
        y2fontsize = float(self.ref_y2fontsize.get())
        titlefontsize = float(self.ref_titlefontsize.get())
        self.trajectory = StackedTrajectoryMaker(self.all_data, self.subframeleft, self.figtitle, self.ref_color1.get(), 
                                          self.ref_color2.get(), self.ref_color3.get(), self.ref_title.get(), titlefontsize,
                                          self.ref_x.get(), xfontsize, self.ref_x2.get(), x2fontsize, self.ref_y.get(), yfontsize, self.ref_y2.get(),
                                          y2fontsize, float(self.ref_height.get()), float(self.ref_width.get()), xmax, xmin, ymax, 
                                          ymin, y2max, y2min)

    # type checks the designation of x/y mins and maxes
    # - val: value input into x/y min or max entry boxes
    def checkMinMax(self, val):
        if val != 'None':
            val = float(val)
        else:
            val = None
        return val
    
    
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
        self.ref_qual.set('Medium')

        self.combo9 = tk.OptionMenu(self.win, self.ref_qual, *refqual)
        self.combo9.config(width=5)
        self.combo9.grid(row=1, column=1, sticky="w", padx=(0, 10), pady="10")


        self.saveButton = tk.Button(self.win, text="SAVE", command=self.save)
        self.saveButton.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)
        #self.win.mainloop()
    
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