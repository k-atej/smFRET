import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from histogramMaker import *
from stackedHistogramMaker import *
from tableMaker import *
import os

#Example MacOS filepath
path = "/Users/katejackson/Desktop/Thrombin Aptamer/Apr15_11"
savefilename = "FREThistogram_stacked.png"
filename = "FRETresult.dat"

#YOU MUST PROVIDE THE EXACT FILE PATH FOR THIS TO WORK

#opens a window that displays a stacked histogram based on the files procided
class StackedHistApplication(tk.Tk):

    # path - filepath provided in entry box in main menu
    # title - name to set as the window title
    def __init__(self, path, title):
        super().__init__()
        self.title(title)
        self.minsize(200, 200)
        self.path = path
        self.savepath = path

        self.find_files()

        #setting up the layout of the window!

        #full window 
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)

        # histogram window
        self.subframeright = tk.Frame(self.frame, background='white')
        self.subframeright.grid(row=0, column=1)

        #window 0
        self.window0 = tk.Frame(self.subframeright, background='white')
        self.window0.grid(row=0, column=0)

        #window 1
        self.window1 = tk.Frame(self.subframeright, background='white')
        self.window1.grid(row=0, column=1, rowspan=3)

        # upper half of window0
        self.subframe2 = tk.Frame(self.window0, background='white')
        self.subframe2.grid(row=0, column=0)
        
        # middle of window0
        self.subframe3 = tk.Frame(self.window0, background='white')
        self.subframe3.grid(row=1, column=0)

        # bottom of window0
        self.subframe4 = tk.Frame(self.window0, background='white')
        self.subframe4.grid(row=2, column=0)
        
        self.start()

    # parses the folders into list of folders with the designated filename in them
    def find_files(self):
        keys = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(filename):
                    key, value = os.path.split(root)
                    keys.append(value)
        
        self.files = []
        for key in keys:
            self.files.append(self.path + "/" + key)

# initializes an empty histogram and creates the customizability options in the side menu
    def start(self):
        self.emptyHis()
        self.makeFeatures()

# creates the dropdowns & buttons available in the customizability menu, binds 'Enter' to the generation of a histogram
    def makeFeatures(self):
        self.makeFormat()
        self.makeOptions()
        self.makeButtons()
        self.bind('<Return>', self.his)
        self.his()

    # sets up the layout of the customizability menu
    def makeFormat(self):
        self.tabControl = ttk.Notebook(master=self.window1)
        self.tabFormat = tk.Frame(self.tabControl)
        self.tabStyle = tk.Frame(self.tabControl)
        self.tabText = tk.Frame(self.tabControl)

        self.tabControl.add(self.tabFormat, text="Format")
        self.tabControl.add(self.tabStyle, text="Style")
        self.tabControl.add(self.tabText, text="Text")
        self.tabControl.grid(row=0, column=0, rowspan=3, padx=10)

        self.tabFormat_0 = tk.Frame(self.tabFormat)
        self.tabFormat_0.grid(row=0, column = 0)
        self.tabFormat_1 = tk.Frame(self.tabFormat)
        self.tabFormat_1.grid(row=1, column = 0)
        self.tabFormat_2 = tk.Frame(self.tabFormat)
        self.tabFormat_2.grid(row=2, column = 0)

        self.tabStyle_0 = tk.Frame(self.tabStyle)
        self.tabStyle_0.grid(row=0, column = 0)
        self.tabStyle_1 = tk.Frame(self.tabStyle)
        self.tabStyle_1.grid(row=1, column = 0)
        self.tabStyle_2 = tk.Frame(self.tabStyle)
        self.tabStyle_2.grid(row=2, column = 0)

        self.tabText_0 = tk.Frame(self.tabText)
        self.tabText_0.grid(row=0, column = 0)
        self.tabText_1 = tk.Frame(self.tabText)
        self.tabText_1.grid(row=1, column = 0)
        self.tabText_2 = tk.Frame(self.tabText)
        self.tabText_2.grid(row=2, column = 0)

    # sets up the generate and clear buttons beneath the histogram
    def makeButtons(self):
        makeHist = tk.Button(self.subframe3, text="Generate", command=self.his)
        makeHist.grid(row=0, column=0, padx="10")

        self.clearButton = tk.Button(self.subframe3, text="Clear", command=self.emptyHis)
        self.clearButton.grid(row=0, column=2, sticky="ew", padx="10", pady="10")

        # save button
        self.saveButton = tk.Button(self.subframe3, text="Save", command=self.savewindow)
        self.saveButton.grid(row=0, column=4, sticky="ew", padx="10", pady="10")

    # sets up options in the customizability window
    def makeOptions(self):

        # first tab = format

        # dropdown menu that allows selection of column in the dataframe, defaults to "eFRET," which is the first column
        self.lbl_label = tk.Label(self.tabFormat_0, text="Data Column:")
        self.lbl_label.grid(row=0, column=0)
        labels = ["eFRET", "other"]
        self.ref_col = tk.StringVar(self)
        self.ref_col.set("eFRET")

        self.combo = tk.OptionMenu(self.tabFormat_0, self.ref_col, *labels)
        self.combo.config(width=10)
        self.combo.grid(row=0, column=1)

        # input area that allows entry of the preferred number of bins to use in the histogram
        self.bin_label = tk.Label(self.tabFormat_1, text="Bins:")
        self.bin_label.grid(row=0, column=0, columnspan=2)
        self.ref_bins = tk.StringVar(self)
        self.ref_bins.set("Auto")

        self.combo1 = tk.Entry(self.tabFormat_1, textvariable=self.ref_bins)
        self.combo1.config(width=10)
        self.combo1.grid(row=0, column=2, sticky="ew", padx=(0, 0), pady="10", columnspan=2)

        # input area that allows entry of the distance to shift data to the left (zeroing)
        self.offset_label = tk.Label(self.tabFormat_2, text="Offset:")
        self.offset_label.grid(row=0, column=0, columnspan=2)
        self.ref_offset = tk.StringVar(self)
        self.ref_offset.set('0.0')

        self.combo3 = tk.Entry(self.tabFormat_2, textvariable=self.ref_offset)
        self.combo3.config(width=10)
        self.combo3.grid(row=0, column=2, sticky="ew", padx=(0, 0), pady="10", columnspan=2)

        # input area to designate maximum value on x axis
        self.xmax_label = tk.Label(self.tabFormat_2, text="X Max:")
        self.xmax_label.grid(row=1, column=0)
        self.ref_xmax = tk.StringVar(self)
        self.ref_xmax.set('None')

        self.comboxmax = tk.Entry(self.tabFormat_2, textvariable=self.ref_xmax)
        self.comboxmax.config(width=5)
        self.comboxmax.grid(row=1, column=1, sticky="ew", padx=(0, 0), pady="10")

        # input area to designate minimum value on x axis
        self.xmin_label = tk.Label(self.tabFormat_2, text="X Min:")
        self.xmin_label.grid(row=2, column=0)
        self.ref_xmin = tk.StringVar(self)
        self.ref_xmin.set('None')

        self.comboxmin = tk.Entry(self.tabFormat_2, textvariable=self.ref_xmin)
        self.comboxmin.config(width=5)
        self.comboxmin.grid(row=2, column=1, sticky="ew", padx=(0, 0), pady="10")

        # input area to designate maximum value on y axis
        self.ymax_label = tk.Label(self.tabFormat_2, text="Y Max:")
        self.ymax_label.grid(row=1, column=2)
        self.ref_ymax = tk.StringVar(self)
        self.ref_ymax.set('None')

        self.comboymax = tk.Entry(self.tabFormat_2, textvariable=self.ref_ymax)
        self.comboymax.config(width=5)
        self.comboymax.grid(row=1, column=3, sticky="ew", padx=(0, 10), pady="10")

        # input area to designate minimum value on y axis
        self.ymin_label = tk.Label(self.tabFormat_2, text="Y Min:")
        self.ymin_label.grid(row=2, column=2)
        self.ref_ymin = tk.StringVar(self)
        self.ref_ymin.set('None')

        self.comboymin = tk.Entry(self.tabFormat_2, textvariable=self.ref_ymin)
        self.comboymin.config(width=5)
        self.comboymin.grid(row=2, column=3, sticky="ew", padx=(0, 10), pady="10")

        # input area for figure width
        self.width_label = tk.Label(self.tabFormat_2, text="Width:")
        self.width_label.grid(row=3, column=0)
        self.ref_width = tk.StringVar(self)
        self.ref_width.set('5')

        self.combowidth = tk.Entry(self.tabFormat_2, textvariable=self.ref_width)
        self.combowidth.config(width=5)
        self.combowidth.grid(row=3, column=1, sticky="ew", padx=(0, 10), pady="10")

         # input area for figure height
        self.height_label = tk.Label(self.tabFormat_2, text="Height:")
        self.height_label.grid(row=3, column=2)
        self.ref_height = tk.StringVar(self)
        self.ref_height.set('5')

        self.comboheight = tk.Entry(self.tabFormat_2, textvariable=self.ref_height)
        self.comboheight.config(width=5)
        self.comboheight.grid(row=3, column=3, sticky="ew", padx=(0, 10), pady="10")



        # second tab = style

        # input area for designation of column fill color
        self.color_label = tk.Label(self.tabStyle_0, text="Color:")
        self.color_label.grid(row=0, column=0)
        self.ref_color = tk.StringVar(self)
        self.ref_color.set("0")

        self.combo2 = tk.Entry(self.tabStyle_0, textvariable=self.ref_color)
        self.combo2.config(width=5)
        self.combo2.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady="10")

        # input area for designation of column edge color
        self.edgecolor_label = tk.Label(self.tabStyle_1, text="Edge Color:")
        self.edgecolor_label.grid(row=1, column=0)
        self.ref_edgecolor = tk.StringVar(self)
        self.ref_edgecolor.set("0")

        self.combo5 = tk.Entry(self.tabStyle_1, textvariable=self.ref_edgecolor)
        self.combo5.config(width=5)
        self.combo5.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="10")

        # input area for designation of column edge line width
        self.edgewidth_label = tk.Label(self.tabStyle_1, text="Edge Width:")
        self.edgewidth_label.grid(row=1, column=2)
        self.ref_edgewidth = tk.StringVar(self)
        self.ref_edgewidth.set("1")

        self.combo6 = tk.Entry(self.tabStyle_1, textvariable=self.ref_edgewidth)
        self.combo6.config(width=5)
        self.combo6.grid(row=1, column=3, sticky="ew", padx=(0, 10), pady="10")

        # third tab: text

        # input area for designation of graph title
        self.title_label = tk.Label(self.tabText_0, text="Title:")
        self.title_label.grid(row=0, column=0)
        self.ref_title = tk.StringVar(self)
        self.ref_title.set("Title")

        self.combo2 = tk.Entry(self.tabText_0, textvariable=self.ref_title)
        self.combo2.config(width=10)
        self.combo2.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady="10")

        #input area for designation of graph title font size
        self.titlefontsize_label = tk.Label(self.tabText_0, text="Title Font Size:")
        self.titlefontsize_label.grid(row=1, column=0)
        self.ref_titlefontsize = tk.StringVar(self)
        self.ref_titlefontsize.set("12")

        self.combo0 = tk.Entry(self.tabText_0, textvariable=self.ref_titlefontsize)
        self.combo0.config(width=10)
        self.combo0.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="10")

        # input area for designation of x-axis label
        self.x_label = tk.Label(self.tabText_1, text="X-Axis Label:")
        self.x_label.grid(row=0, column=0)
        self.ref_x = tk.StringVar(self)
        self.ref_x.set("X-Axis")

        self.combo2 = tk.Entry(self.tabText_1, textvariable=self.ref_x)
        self.combo2.config(width=10)
        self.combo2.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady="10")

        # input area for designation of y-axis label
        self.y_label = tk.Label(self.tabText_2, text="Y-Axis Label:")
        self.y_label.grid(row=0, column=0)
        self.ref_y = tk.StringVar(self)
        self.ref_y.set("Y-Axis")

        self.combo2 = tk.Entry(self.tabText_2, textvariable=self.ref_y)
        self.combo2.config(width=10)
        self.combo2.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady="10")

        # input area for designation of x-axis font size
        self.xfontsize_label = tk.Label(self.tabText_1, text="X Font Size:")
        self.xfontsize_label.grid(row=1, column=0)
        self.ref_xfontsize = tk.StringVar(self)
        self.ref_xfontsize.set("10")

        self.combo7 = tk.Entry(self.tabText_1, textvariable=self.ref_xfontsize)
        self.combo7.config(width=10)
        self.combo7.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="10")

        # input area for designation of y-axis font size
        self.yfontsize_label = tk.Label(self.tabText_2, text="Y Font Size:")
        self.yfontsize_label.grid(row=1, column=0)
        self.ref_yfontsize = tk.StringVar(self)
        self.ref_yfontsize.set("10")

        self.combo8 = tk.Entry(self.tabText_2, textvariable=self.ref_yfontsize)
        self.combo8.config(width=10)
        self.combo8.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="10")

    # generates histogram without data
    def emptyHis(self):
        df_empty = pd.DataFrame({'A' : []})
        self.hist = HistMaker(df_empty, self.savepath, self.subframe2, 0, 0, 1, "None", 12, " ", " ", "b", "b", 1, 1, 0, 1, 0, 10.0, 10.0, 5.0, 5.0, 0)

    # generates a stacked histogram based on the parameters set in the customizability menu
    def his(self, event=None): #creates histogram from sample data
        self.hist.destroy()

        # need to check that this column is present in all files?
        datacol = self.ref_col.get()
        bins = self.ref_bins.get()
        title = str(self.ref_title.get())
        x_ax = str(self.ref_x.get())
        y_ax = str(self.ref_y.get())
        color = str(self.ref_color.get())
        edgecolor = str(self.ref_edgecolor.get())
        edgewidth = float(self.ref_edgewidth.get())
        offset = self.ref_offset.get()
        xmax = self.checkMinMax(self.ref_xmax.get())
        xmin = self.checkMinMax(self.ref_xmin.get())
        ymax = self.checkMinMax(self.ref_ymax.get())
        ymin = self.checkMinMax(self.ref_ymin.get())

        width = float(self.ref_width.get())
        height = float(self.ref_height.get())

        xfontsize = float(self.ref_xfontsize.get())
        yfontsize = float(self.ref_yfontsize.get())
        titlefontsize = float(self.ref_titlefontsize.get())
        self.hist = StackedHistMaker(self.files, self.savepath, datacol, self.subframe2, 0, 0, bins, title, titlefontsize, x_ax, y_ax, color, edgecolor, edgewidth, xmax, xmin, ymax, ymin, xfontsize, yfontsize, width, height, offset)
        self.ref_bins.set(self.hist.getBins())

    # type checks the designation of x/y mins and maxes
    def checkMinMax(self, val):
        if val != 'None':
            val = float(val)
        else:
            val = None
        return val

    
    def savewindow(self):
        self.win = tk.Tk()
        self.win.title("Set Filepath: ")
        
        #input area for file name
        self.path_label = tk.Label(self.win, text="Save File Path:")
        self.path_label.grid(row=0, column=0)
        self.ref_path = tk.StringVar(self.win)
        self.ref_path.set(self.savepath + '/' + savefilename)

        self.combo6 = tk.Entry(self.win, textvariable=self.ref_path)
        self.combo6.config(width=50)
        self.combo6.grid(row=0, column=1, sticky="ew", padx=(10, 10), pady="10")

        self.saveButton = tk.Button(self.win, text="SAVE", command=self.save)
        self.saveButton.grid(row=1, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)
        self.win.mainloop()


    def save(self):
        self.hist.save(self.ref_path.get())
        self.win.destroy()
