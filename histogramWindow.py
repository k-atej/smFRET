import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from matplotlib.figure import Figure
from histogramMaker import *


#Example MacOS filepath
path = "/Users/katejackson/Desktop/Thrombin Aptamer/Apr15_11/(1) THROMBIN APTAMER, 0 mM KCl"


#opens a window that displays a histogram based on the file provided
class HistApplication(tk.Toplevel):

    # path - filepath provided in entry box in main menu
    # title - name to set as the window title
    def __init__(self, path, filename, title):
        super().__init__()
        self.title(title)
        self.minsize(200, 200)
        self.path = path + "/" + filename
        self.savepath = path
        self.annotations =[]
        self.hist = None
        
        self.get_data()

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
           
    # parses the data file into a pandas dataframe
    def get_data(self):
        FRETresult = open(self.path, "r") 
        data = pd.read_fwf(FRETresult, header=None)
        data.columns = ["eFRET", "other"]
        self.df = data

    # initializes an empty histogram and creates the customizability options in the side menu
    def start(self):
        self.makeFeatures()
        self.emptyHis()

    # creates the dropdowns & buttons available in the customizability menu, binds 'Enter' to the generation of a histogram
    def makeFeatures(self):
        self.makeFormat()
        self.makeOptions()
        self.makeButtons()
        self.bind('<Return>', self.his)
        self.bind('<BackSpace>', self.undoLastLine)
        #self.his()
    

    # sets up the layout of the customizability menu
    def makeFormat(self):
        self.tabControl = ttk.Notebook(master=self.window1)
        self.tabFormat = tk.Frame(self.tabControl)
        self.tabStyle = tk.Frame(self.tabControl)
        self.tabText = tk.Frame(self.tabControl)
        #self.tabStyle.bind('<Return>', self.his)
        #self.tabText.bind('<Return>', self.his)

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
        # generate button, bound to the generation of a histogram
        makeHist = tk.Button(self.subframe3, text="Generate", command=self.his)
        makeHist.grid(row=0, column=0, padx="10")

        # clear button, bound to the generation of an empty histogram
        self.clearButton = tk.Button(self.subframe3, text="Clear Lines", command=self.emptyHis)
        self.clearButton.grid(row=0, column=1, sticky="ew", padx="10", pady="10")

        # undo button, bound to the generation of an empty histogram
        self.undoButton = tk.Button(self.subframe3, text="Undo Line", command=self.undoLastLine)
        self.undoButton.grid(row=0, column=2, sticky="ew", padx="10", pady="10")

        # save button
        self.saveButton = tk.Button(self.subframe3, text="Save", command=self.savewindow)
        self.saveButton.grid(row=0, column=3, sticky="ew", padx="10", pady="10")

        #check box for clicking to add lines
        self.linetoggle = tk.IntVar()
        self.toggle1 = tk.Checkbutton(self.subframe3, text="Click to Add Lines", variable=self.linetoggle, onvalue=1, offvalue=0)
        self.toggle1.grid(row=0, column=4, sticky="ew", padx=(10,10), pady="10", columnspan=2)
        

    # sets up options in the customizability window
    def makeOptions(self):

        # first tab = format

        # dropdown menu that allows selection of column in the dataframe, defaults to "eFRET," which is the first column
        self.lbl_label = tk.Label(self.tabFormat_0, text="Data Column:")
        self.lbl_label.grid(row=0, column=0)
        labels = self.df.columns
        self.ref_col = tk.StringVar(self)
        self.ref_col.set("eFRET")

        self.combo = tk.OptionMenu(self.tabFormat_0, self.ref_col, *labels)
        self.combo.config(width=10)
        self.combo.grid(row=0, column=1)

        # input area that allows entry of the preferred number of bins to use in the histogram
        # any value less than 1 will be considered the "bin width" and # of bins will be calculated and displayed
        self.bin_label = tk.Label(self.tabFormat_1, text="Bin Number:")
        self.bin_label.grid(row=1, column=0)
        self.ref_bins = tk.StringVar(self)
        self.ref_bins.set("10")

        #check box for toggling binwidth/bin num
        self.bin2 = tk.IntVar()
        self.toggle2 = tk.Checkbutton(self.tabFormat_1, text="Bin Num", variable=self.bin2, onvalue=1, offvalue=0, command=self.togglebins)
        self.toggle2.grid(row=0, column=2, sticky="ew", padx=(10,10), pady="10")
        self.bin2.set(1)


        #check box for toggling binwidth/bin num
        self.bin1 = tk.IntVar()
        self.toggle1 = tk.Checkbutton(self.tabFormat_1, text="Bin Width", variable=self.bin1, onvalue=1, offvalue=0, command=self.changeLabel)
        self.toggle1.grid(row=0, column=0, sticky="ew", padx=(10,10), pady="10")
        
        
       
        self.combo1 = tk.Entry(self.tabFormat_1, textvariable=self.ref_bins)
        self.combo1.config(width=10)
        self.combo1.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="10")

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

        self.colorbutton = tk.Button(self.tabStyle_0, text="Select Color", command=self.choose_fillcolor)
        self.colorbutton.grid(row=0, column=3)

        # input area for designation of column edge color
        self.edgecolor_label = tk.Label(self.tabStyle_1, text="Edge Color:")
        self.edgecolor_label.grid(row=1, column=0)
        self.ref_edgecolor = tk.StringVar(self)
        self.ref_edgecolor.set("0")

        self.combo5 = tk.Entry(self.tabStyle_1, textvariable=self.ref_edgecolor)
        self.combo5.config(width=5)
        self.combo5.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="10")

        self.edgecolorbutton = tk.Button(self.tabStyle_1, text='Select Color', command=self.choose_edgecolor)
        self.edgecolorbutton.grid(row=1, column=2)

        # dropdown for designation of column edge line width
        self.edgewidth_label = tk.Label(self.tabStyle_1, text="Edge Width:")
        self.edgewidth_label.grid(row=2, column=0)
        refedge = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
        self.ref_edgewidth = tk.StringVar(self)
        self.ref_edgewidth.set(1.0)

        self.combo6 = tk.OptionMenu(self.tabStyle_1, self.ref_edgewidth, *refedge)
        self.combo6.config(width=5)
        self.combo6.grid(row=2, column=1, sticky="ew", padx=(0, 10), pady="10")



        # input area for designation of line color
        self.linecolor_label = tk.Label(self.tabStyle_2, text="Line Color:")
        self.linecolor_label.grid(row=0, column=0)
        self.ref_linecolor = tk.StringVar(self)
        self.ref_linecolor.set("red")

        self.combol = tk.Entry(self.tabStyle_2, textvariable=self.ref_linecolor)
        self.combol.config(width=5)
        self.combol.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady="10")

        self.linecolorbutton = tk.Button(self.tabStyle_2, text='Select Color', command=self.choose_linecolor)
        self.linecolorbutton.grid(row=0, column=2)

        # dropdown for designation of line style
        self.linestyle_label = tk.Label(self.tabStyle_2, text="Line Style:")
        self.linestyle_label.grid(row=1, column=0)
        refstyle = ["solid", "dashed", "dotted", "dashdot"]
        self.ref_linestyle = tk.StringVar(self)
        self.ref_linestyle.set("dashed")

        self.combo9 = tk.OptionMenu(self.tabStyle_2, self.ref_linestyle, *refstyle)
        self.combo9.config(width=5)
        self.combo9.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="10")

        #dropdown for linewidth
        self.lw_label = tk.Label(self.tabStyle_2, text="Line Width:")
        self.lw_label.grid(row=2, column=0)
        lw = [1.0, 2.0, 3.0, 4.0]
        self.ref_lw = tk.IntVar(self)
        self.ref_lw.set(1.0)

        self.combolw = tk.OptionMenu(self.tabStyle_2, self.ref_lw, *lw)
        self.combolw.config(width=5)
        self.combolw.grid(row=2, column=1)



        # third tab: text

        # input area for designation of graph title
        self.title_label = tk.Label(self.tabText_0, text="Title:")
        self.title_label.grid(row=0, column=0)
        self.ref_title = tk.StringVar(self)
        self.ref_title.set("Title")

        self.combo2 = tk.Entry(self.tabText_0, textvariable=self.ref_title)
        self.combo2.config(width=10)
        self.combo2.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady="10")

        #title font size
        self.titlef_label = tk.Label(self.tabText_0, text="Size:")
        self.titlef_label.grid(row=0, column=2)
        titlef = [8, 10, 12, 15, 20, 24]
        self.ref_titlefontsize = tk.StringVar(self)
        self.ref_titlefontsize.set("12")

        self.combo = tk.OptionMenu(self.tabText_0, self.ref_titlefontsize, *titlef)
        self.combo.config(width=5)
        self.combo.grid(row=0, column=3)


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

        self.combo3 = tk.Entry(self.tabText_2, textvariable=self.ref_y)
        self.combo3.config(width=10)
        self.combo3.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady="10")

        #x font size
        self.titlex_label = tk.Label(self.tabText_1, text="Size:")
        self.titlex_label.grid(row=0, column=2)
        titlex = [8, 10, 12, 15, 20, 24]
        self.ref_xfontsize = tk.StringVar(self)
        self.ref_xfontsize.set("12")

        self.combo4 = tk.OptionMenu(self.tabText_1, self.ref_xfontsize, *titlex)
        self.combo4.config(width=5)
        self.combo4.grid(row=0, column=3)

        #y font size
        self.titley_label = tk.Label(self.tabText_2, text="Size:")
        self.titley_label.grid(row=0, column=2)
        titley = [8, 10, 12, 15, 20, 24]
        self.ref_yfontsize = tk.StringVar(self)
        self.ref_yfontsize.set("12")

        self.combo = tk.OptionMenu(self.tabText_2, self.ref_yfontsize, *titley)
        self.combo.config(width=5)
        self.combo.grid(row=0, column=3)

    # generates histogram without data
    def emptyHis(self):
        #df_empty = pd.DataFrame({'A' : []})
        #self.hist = HistMaker(df_empty, self.savepath, self.subframe2, 0, 0, 1, 0, "None", 12, " ", " ", "b", "b", 1, 1, 0, 1, 0, 10.0, 10.0,  5.0, 5.0, [], 0)
        self.annotations = []
        self.his()

    # generates a histogram based on the parameters set in the customizability menu
    def his(self, event=None): 

        if self.hist is not None:
            self.hist.destroy()

        col = self.ref_col.get()
        bins = self.ref_bins.get()
        title = str(self.ref_title.get())
        x_ax = str(self.ref_x.get())
        y_ax = str(self.ref_y.get())
        
        color = str(self.ref_color.get())
        if color == "None":
            color = 0

        edgecolor = str(self.ref_edgecolor.get())
        if edgecolor == "None":
            edgecolor = 0

        linecolor = str(self.ref_linecolor.get())
        if linecolor == "None":
            linecolor = "red"

        linestyle = self.ref_linestyle.get()
        linetogg = self.linetoggle.get()
        linewidth = self.ref_lw.get()
        edgewidth = float(self.ref_edgewidth.get())
        offset = self.ref_offset.get()
        xmax = self.checkMinMax(self.ref_xmax.get())
        xmin = self.checkMinMax(self.ref_xmin.get())
        ymax = self.checkMinMax(self.ref_ymax.get())
        ymin = self.checkMinMax(self.ref_ymin.get())

        width = float(self.ref_width.get())
        height = float(self.ref_height.get())

        bin1 = self.bin1.get()

        xfontsize = float(self.ref_xfontsize.get())
        yfontsize = float(self.ref_yfontsize.get())
        titlefontsize = float(self.ref_titlefontsize.get())
        self.hist = HistMaker(self.df[col], self.savepath, self.subframe2, 0, 0, bins, bin1, title, titlefontsize, x_ax, y_ax, color, edgecolor, edgewidth, xmax, xmin, ymax, ymin, xfontsize, yfontsize, width, height, self.annotations, linecolor, linestyle, linetogg, linewidth, offset)
        self.ref_bins.set(self.hist.getBins())
        self.annotations = self.hist.getAnnotations()

    # type checks the designation of x/y mins and maxes
    def checkMinMax(self, val):
        if val != 'None':
            val = float(val)
        else:
            val = None
        return val
    
    # currently unused, can create an empty figure to take up space
    def emptyFig(self):
        fig = Figure()
        canvas = FigureCanvasTkAgg(fig, master=self.subframe2)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1)

    def savewindow(self):
        self.win = tk.Toplevel()
        self.win.title("Set Filepath: ")
        
        #input area for file name
        s = ""
        savepath = self.path.split(".")
        for path in savepath[:-1]:
            s+= path
        self.path_label = tk.Label(self.win, text="Save File Path:")
        self.path_label.grid(row=0, column=0)
        self.ref_path = tk.StringVar(self.win)
        self.ref_path.set(s)

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
        self.hist.save(self.ref_path.get(), self.ref_type.get())
        self.win.destroy()
        

    def changeLabel(self):
            if self.bin1.get() == 1:
                self.bin_label = tk.Label(self.tabFormat_1, text="Bin Width:")
                self.bin_label.grid(row=1, column=0)
                self.bin2.set(0)

            elif self.bin1.get() == 0:
                self.bin_label = tk.Label(self.tabFormat_1, text="Bin Number:")
                self.bin_label.grid(row=1, column=0)
            else:
                self.bin_label = tk.Label(self.tabFormat_1, text="Error! ")
                self.bin_label.grid(row=1, column=0)

    def choose_fillcolor(self):
        color_code, hexcode = colorchooser.askcolor(title="Choose Color")
        self.ref_color.set(hexcode)

    def choose_edgecolor(self):
        color_code, hexcode = colorchooser.askcolor(title="Choose Color")
        self.ref_edgecolor.set(hexcode)
    
    def choose_linecolor(self):
        color_code, hexcode = colorchooser.askcolor(title="Choose Color")
        self.ref_linecolor.set(hexcode)

    def undoLastLine(self, event=None):
        if len(self.annotations) > 0:
            self.annotations.pop()
            self.his()

    def togglebins(self):
        self.bin1.set(0)
        self.changeLabel()