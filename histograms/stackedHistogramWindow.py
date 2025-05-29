import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from histograms.histogramMaker import *
from histograms.stackedHistogramMaker import *
import os

# Example MacOS filepath:
# /Users/katejackson/Desktop/Thrombin Aptamer/Apr15_11 copy

#opens a window that displays a stacked histogram based on the files provided
#   path: filepath provided in entry box in histogram main menu
#   filename: name of file that was being searched for, set in histogram main menu
#   title: name to set as the window title
#   keys: list of full file paths to each file
class StackedHistApplication(tk.Toplevel):

    # initializes variables within the class
    def __init__(self, path, filename, title, keys):
        super().__init__()
        self.title(title)
        self.minsize(200, 200)

        self.path = path
        self.savepath = path
        self.keys = keys

        self.annotations = []
        self.hist = None
        self.filename = filename
        self.subtitle_inputs = []
        self.generation = 0

        # collect each designated file into a list
        self.find_files()

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
        
        # make the window with the histogram and all of the options
        self.start()

    # parses the folders into list of folders with the designated filename in them
    def find_files(self):
        keys = []
        for root, dirs, files in os.walk(self.path):
            dirs.sort()
            for file in sorted(files):
                if file.endswith(self.filename):
                    key, value = os.path.split(root)
                    keys.append(value)
        
        self.files = []
        for key in keys:
            self.files.append(os.path.join(self.path, key))

    # initializes and creates the customizability options in the side menu
    # then makes the histogram
    def start(self):
        self.makeFeatures()
        self.his()
        

    # creates the dropdowns & buttons available in the customizability menu, 
    # binds 'Enter' to the generation of a histogram
    # bins 'Backspace' to line deletions
    def makeFeatures(self):
        self.makeFormat()
        self.makeOptions()
        self.makeButtons()
        self.bind('<Return>', self.his)
        self.bind('<BackSpace>', self.undoLastLine)

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

        # generate button, bound to the generation of a histogram
        makeHist = tk.Button(self.subframe3, text="Generate", command=self.his)
        makeHist.grid(row=0, column=0, padx="10")

        # clear button, clears all lines on histogram and regenerates histogram
        self.clearButton = tk.Button(self.subframe3, text="Clear Lines", command=self.emptyHis)
        self.clearButton.grid(row=0, column=1, sticky="ew", padx="10", pady="10")

        # undo button, removes last line on histogram and regenerates histogram
        self.undoButton = tk.Button(self.subframe3, text="Undo Line", command=self.undoLastLine)
        self.undoButton.grid(row=0, column=2, sticky="ew", padx="10", pady="10")

        # save button, generates new save window to insert file path to save at
        self.saveButton = tk.Button(self.subframe3, text="Save", command=self.savewindow)
        self.saveButton.grid(row=0, column=3, sticky="ew", padx="10", pady="10")

        #check box, toggles on click-to-add lines
        self.linetoggle = tk.IntVar()
        self.toggle1 = tk.Checkbutton(self.subframe3, text="Click to Add Lines", variable=self.linetoggle, onvalue=1, offvalue=0)
        self.toggle1.grid(row=0, column=4, sticky="ew", padx=(10,10), pady="10", columnspan=2)

        self.lbl_label = tk.Label(self.subframe3, text="Double Click to add full lines")
        self.lbl_label.grid(row=1, column=3, columnspan=3)

    # sets up options in the customizability window
    def makeOptions(self):

        # first tab = format

        self.data_label = tk.Label(self.tabFormat, text="Data:")
        self.data_label.grid(row=0, column=0, pady="5", padx=(5), sticky="w")

        # dropdown menu that allows selection of column in the dataframe, defaults to "eFRET," which is the first column
        self.lbl_label = tk.Label(self.tabFormat, text="Source:")
        self.lbl_label.grid(row=1, column=0, padx=(20,0), pady="5")
        labels = ["eFRET", "other"]
        self.ref_col = tk.StringVar(self)
        self.ref_col.set("eFRET")

        self.combo = tk.OptionMenu(self.tabFormat, self.ref_col, *labels)
        self.combo.config(width=5)
        self.combo.grid(row=1, column=1, columnspan=1)

        self.binning_label = tk.Label(self.tabFormat, text="Bins:")
        self.binning_label.grid(row=3, column=0, pady="5", padx="5", sticky="w")

        # input area that allows entry of the preferred number of bins or bin width to use in the histogram (depends on bin1 and bin2)
        self.bin_label = tk.Label(self.tabFormat, text="Bins:")
        self.bin_label.grid(row=5, column=0, pady="5", padx=(20,0), sticky="w")
        self.ref_bins = tk.StringVar(self)
        self.ref_bins.set("10")

        #check box for toggling to bin number input
        self.bin2 = tk.IntVar()
        self.toggle2 = tk.Checkbutton(self.tabFormat, text="Bin Number", variable=self.bin2, onvalue=1, offvalue=0, command=self.togglebins)
        self.toggle2.grid(row=4, column=2, sticky="w", padx=(0,0), pady="5", columnspan=2)
        self.bin2.set(1)

        #check box for toggling to bin width input
        self.bin1 = tk.IntVar()
        self.toggle1 = tk.Checkbutton(self.tabFormat, text="Bin Width", variable=self.bin1, onvalue=1, offvalue=0, command=self.changeLabel)
        self.toggle1.grid(row=4, column=0, sticky="w", padx=(20,0), pady="5", columnspan=2)
       
        self.combo1 = tk.Entry(self.tabFormat, textvariable=self.ref_bins)
        self.combo1.config(width=5)
        self.combo1.grid(row=5, column=1, padx=(0, 10), pady="5", sticky="w")

        # input area that allows entry of the distance to shift data to the left (zeroing)
        self.offset_label = tk.Label(self.tabFormat, text="Offset:")
        self.offset_label.grid(row=2, column=0, padx=(15,0), sticky="ew", pady="5")
        self.ref_offset = tk.StringVar(self)
        self.ref_offset.set('0.0')

        self.combo3 = tk.Entry(self.tabFormat, textvariable=self.ref_offset)
        self.combo3.config(width=5)
        self.combo3.grid(row=2, column=1, pady="5", sticky="w")

        self.fig_label = tk.Label(self.tabFormat, text="Figure:")
        self.fig_label.grid(row=6, column=0, pady="5", padx="5", sticky="w")
        
        # input area to designate maximum value on x axis
        self.xmax_label = tk.Label(self.tabFormat, text="X Max:")
        self.xmax_label.grid(row=8, column=2)
        self.ref_xmax = tk.StringVar(self)
        self.ref_xmax.set('None')

        self.comboxmax = tk.Entry(self.tabFormat, textvariable=self.ref_xmax)
        self.comboxmax.config(width=5)
        self.comboxmax.grid(row=8, column=3, sticky="w", padx=(0, 0), pady="5")

        # input area to designate minimum value on x axis
        self.xmin_label = tk.Label(self.tabFormat, text="X Min:")
        self.xmin_label.grid(row=8, column=0, sticky="w", padx=(20,0), pady="5")
        self.ref_xmin = tk.StringVar(self)
        self.ref_xmin.set('None')

        self.comboxmin = tk.Entry(self.tabFormat, textvariable=self.ref_xmin)
        self.comboxmin.config(width=5)
        self.comboxmin.grid(row=8, column=1, sticky="w", padx=(0, 0), pady="5")

        # input area to designate maximum value on y axis
        self.ymax_label = tk.Label(self.tabFormat, text="Y Max:")
        self.ymax_label.grid(row=9, column=2)
        self.ref_ymax = tk.StringVar(self)
        self.ref_ymax.set('None')

        self.comboymax = tk.Entry(self.tabFormat, textvariable=self.ref_ymax)
        self.comboymax.config(width=5)
        self.comboymax.grid(row=9, column=3, sticky="w", padx=(0, 0), pady="5")

        # input area to designate minimum value on y axis
        self.ymin_label = tk.Label(self.tabFormat, text="Y Min:")
        self.ymin_label.grid(row=9, column=0, sticky="w", padx=(20,0), pady="5")
        self.ref_ymin = tk.StringVar(self)
        self.ref_ymin.set('None')

        self.comboymin = tk.Entry(self.tabFormat, textvariable=self.ref_ymin)
        self.comboymin.config(width=5)
        self.comboymin.grid(row=9, column=1, sticky="w", padx=(0, 10), pady="5")

        # input area for figure width
        self.width_label = tk.Label(self.tabFormat, text="Width:")
        self.width_label.grid(row=7, column=0, sticky="w", padx=(20,0), pady="5")
        self.ref_width = tk.StringVar(self)
        self.ref_width.set('5')

        self.combowidth = tk.Entry(self.tabFormat, textvariable=self.ref_width)
        self.combowidth.config(width=5)
        self.combowidth.grid(row=7, column=1, sticky="w", padx=(0, 10), pady="5")

         # input area for figure height
        self.height_label = tk.Label(self.tabFormat, text="Height:")
        self.height_label.grid(row=7, column=2)
        self.ref_height = tk.StringVar(self)
        self.ref_height.set('5')

        self.comboheight = tk.Entry(self.tabFormat, textvariable=self.ref_height)
        self.comboheight.config(width=5)
        self.comboheight.grid(row=7, column=3, sticky="w", padx=(0, 5), pady="5")



        # second tab = style

        self.fig_label = tk.Label(self.tabStyle, text="Histogram:")
        self.fig_label.grid(row=0, column=0, pady="5", padx="5", sticky="w")

        # input area for designation of histogram fill color
        self.color_label = tk.Label(self.tabStyle, text="Fill Color:")
        self.color_label.grid(row=1, column=0, sticky="w", padx=(20,0), pady="5")
        self.ref_color = tk.StringVar(self)
        self.ref_color.set("0")

        self.combo2 = tk.Entry(self.tabStyle, textvariable=self.ref_color)
        self.combo2.config(width=8)
        self.combo2.grid(row=1, column=1, padx=(0, 10), pady="5", sticky="w")

        # color wheel for designation of histogram fill color
        self.colorbutton = tk.Button(self.tabStyle, text="Select", command=self.choose_fillcolor)
        self.colorbutton.grid(row=1, column=2)

        # input area for designation of column edge color
        self.edgecolor_label = tk.Label(self.tabStyle, text="Edge Color:")
        self.edgecolor_label.grid(row=2, column=0, sticky="w", padx=(20,0), pady="5")
        self.ref_edgecolor = tk.StringVar(self)
        self.ref_edgecolor.set("0")

        self.combo5 = tk.Entry(self.tabStyle, textvariable=self.ref_edgecolor)
        self.combo5.config(width=8)
        self.combo5.grid(row=2, column=1, padx=(0, 10), pady="5", sticky="w")

        # color wheel for designation of histogram edge color
        self.edgecolorbutton = tk.Button(self.tabStyle, text='Select', command=self.choose_edgecolor)
        self.edgecolorbutton.grid(row=2, column=2)

        # dropdown for designation of column edge line width
        self.edgewidth_label = tk.Label(self.tabStyle, text="Edge Width:")
        self.edgewidth_label.grid(row=3, column=0, sticky="w", padx=(20, 10), pady="5")
        refedge = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
        self.ref_edgewidth = tk.StringVar(self)
        self.ref_edgewidth.set(1.0)

        self.combo6 = tk.OptionMenu(self.tabStyle, self.ref_edgewidth, *refedge)
        self.combo6.config(width=4)
        self.combo6.grid(row=3, column=1, sticky="w", padx=(0, 10), pady="5")


        self.hist_label = tk.Label(self.tabStyle, text="Line Annotations:")
        self.hist_label.grid(row=5, column=0, pady=(10,5), padx="5", sticky="w", columnspan=2)

        # input area for designation of click-to-add vertical line color
        self.linecolor_label = tk.Label(self.tabStyle, text="Line Color:")
        self.linecolor_label.grid(row=6, column=0, sticky="w", padx=(20,0), pady="5")
        self.ref_linecolor = tk.StringVar(self)
        self.ref_linecolor.set("red")

        self.combol = tk.Entry(self.tabStyle, textvariable=self.ref_linecolor)
        self.combol.config(width=8)
        self.combol.grid(row=6, column=1, sticky="w", padx=(0, 10), pady="5")

        # color wheel for designation of click-to-add vertical line color
        self.linecolorbutton = tk.Button(self.tabStyle, text='Select', command=self.choose_linecolor)
        self.linecolorbutton.grid(row=6, column=2)

        # dropdown for designation of line style
        self.linestyle_label = tk.Label(self.tabStyle, text="Line Style:")
        self.linestyle_label.grid(row=7, column=0, sticky="w", padx=(20,0), pady="5")
        refstyle = ["solid", "dashed", "dotted", "dashdot"]
        self.ref_linestyle = tk.StringVar(self)
        self.ref_linestyle.set("dashed")

        self.combo9 = tk.OptionMenu(self.tabStyle, self.ref_linestyle, *refstyle)
        self.combo9.config(width=4)
        self.combo9.grid(row=7, column=1, sticky="w", padx=(0, 10), pady="5")

        #dropdown for linewidth
        self.lw_label = tk.Label(self.tabStyle, text="Line Width:")
        self.lw_label.grid(row=8, column=0, sticky="w", padx=(20,0), pady="5")
        lw = [1.0, 2.0, 3.0, 4.0]
        self.ref_lw = tk.IntVar(self)
        self.ref_lw.set(1.0)

        self.combolw = tk.OptionMenu(self.tabStyle, self.ref_lw, *lw)
        self.combolw.config(width=4)
        self.combolw.grid(row=8, column=1, sticky="w", padx=(0, 10), pady="5")


        
        #check box for toggling zero on y axis
        self.toggle = tk.IntVar()
        self.toggle1 = tk.Checkbutton(self.tabStyle, text="Toggle Zero on Y-Axis", variable=self.toggle, onvalue=1, offvalue=0)
        self.toggle1.grid(row=4, column=0, sticky="w", padx=(20,0), pady=(5), columnspan=2)




        
        # third tab: text

        # input area for designation of graph title
        self.title_label = tk.Label(self.tabText, text="Title:")
        self.title_label.grid(row=0, column=0, sticky="w", padx=(5,0), pady="5")
        self.ref_title = tk.StringVar(self)
        self.ref_title.set("Title")

        self.combo2 = tk.Entry(self.tabText, textvariable=self.ref_title)
        self.combo2.config(width=15)
        self.combo2.grid(row=0, column=1, sticky="w", padx=(0, 10), pady="5")

        # dropdown for title font size
        titlef = [8, 9, 10, 11, 12, 15, 20, 24]
        self.ref_titlefontsize = tk.StringVar(self)
        self.ref_titlefontsize.set("12")

        self.combo = tk.OptionMenu(self.tabText, self.ref_titlefontsize, *titlef)
        self.combo.config(width=2)
        self.combo.grid(row=0, column=2)

   
        self.hist_label = tk.Label(self.tabText, text="Axis Labels:")
        self.hist_label.grid(row=1, column=0, pady=(10,5), padx="5", sticky="w", columnspan=2)

        # input area for designation of x-axis label
        self.x_label = tk.Label(self.tabText, text="X:")
        self.x_label.grid(row=2, column=0, sticky="w", padx=(20,0), pady="5")
        self.ref_x = tk.StringVar(self)
        self.ref_x.set("FRET Efficiency")

        self.combo2 = tk.Entry(self.tabText, textvariable=self.ref_x)
        self.combo2.config(width=15)
        self.combo2.grid(row=2, column=1, sticky="w", padx=(0, 10), pady="5")

        # input area for designation of y-axis label
        self.y_label = tk.Label(self.tabText, text="Y:")
        self.y_label.grid(row=3, column=0, sticky="w", padx=(20,0), pady="5")
        self.ref_y = tk.StringVar(self)
        self.ref_y.set("Count")

        self.combo3 = tk.Entry(self.tabText, textvariable=self.ref_y)
        self.combo3.config(width=15)
        self.combo3.grid(row=3, column=1, sticky="w", padx=(0, 10), pady="5")

        # dropdown for x font size
        titlex = [8, 9, 10, 11, 12, 15, 20, 24]
        self.ref_xfontsize = tk.StringVar(self)
        self.ref_xfontsize.set("12")

        self.combo4 = tk.OptionMenu(self.tabText, self.ref_xfontsize, *titlex)
        self.combo4.config(width=2)
        self.combo4.grid(row=2, column=2)

        # dropdown for y font size
        titley = [8, 9, 10, 11, 12, 15, 20, 24]
        self.ref_yfontsize = tk.StringVar(self)
        self.ref_yfontsize.set("12")

        self.combo = tk.OptionMenu(self.tabText, self.ref_yfontsize, *titley)
        self.combo.config(width=2)
        self.combo.grid(row=3, column=2)


    # generates histogram without line annotations
    def emptyHis(self):
        self.annotations = []
        self.his()

    # generates a histogram based on the parameters set in the customizability menu
    def his(self, event=None): 

        # clear any existing histogram
        if self.hist is not None:
            self.hist.destroy()
        self.generation += 1

        # collect and check parameters from the customization menus
        color = str(self.ref_color.get())
        if color == "None":
            color = "black"

        edgecolor = str(self.ref_edgecolor.get())
        if edgecolor == "None":
            edgecolor = "black"
        
        linecolor = str(self.ref_linecolor.get())
        if linecolor == "None":
            linecolor = "red"

        xmax = self.checkMinMax(self.ref_xmax.get())
        xmin = self.checkMinMax(self.ref_xmin.get())
        ymax = self.checkMinMax(self.ref_ymax.get())
        ymin = self.checkMinMax(self.ref_ymin.get())
     
        subtitles = []
        subtitlesizes = []
        for subtitle in self.subtitle_inputs:
            j, jtext, jfontsize = subtitle
            subtitles.append(j.get())
            subtitlesizes.append(jfontsize.get())

         # create the new histogram based on parameters from the customization menu
        self.hist = StackedHistMaker(self.files, self.savepath, self.filename, self.ref_col.get(), self.subframe2, 
                                     0, 0, self.ref_bins.get(), self.bin1.get(), str(self.ref_title.get()), 
                                     float(self.ref_titlefontsize.get()), str(self.ref_x.get()),str(self.ref_y.get()), 
                                     color, edgecolor, float(self.ref_edgewidth.get()), xmax, xmin, ymax, ymin, 
                                     float(self.ref_xfontsize.get()), float(self.ref_yfontsize.get()), float(self.ref_width.get()), 
                                     float(self.ref_height.get()), self.toggle.get(), self.annotations, subtitles, 
                                     subtitlesizes, linecolor, self.ref_linestyle.get(), 
                                     self.linetoggle.get(), self.ref_lw.get(), self.ref_offset.get())
        
        # save annotations & subtitles on histogram
        self.annotations = self.hist.get_annotations()
        self.subtitle_length = self.hist.get_height()
        self.subtitles = self.hist.get_subtitles()
        self.subtitlesizes = self.hist.get_subtitlesizes()
        
        # make input areas for subtitles based on hist size
        if self.generation == 1:
            self.makeSubtitles()

        # set the bin number or width if using auto-binning
        self.ref_bins.set(self.hist.getBins())

        # reset subtitle input sizes
        self.resetSubtitles()

    # reset subtitle input sizes
    def resetSubtitles(self):
        if len(self.subtitle_inputs) == len(self.subtitles):
            for i in range(len(self.subtitle_inputs)):
                j, jtext, jfontsize = self.subtitle_inputs[i]
                jtext.set(self.subtitles[i])
                jfontsize.set(self.subtitlesizes[i])

    # set up inputs based on stacked hist size
    def makeSubtitles(self):
        self.makeSubtitleInputs()
        folders = self.hist.get_lastfolder()
        for i in range(len(self.subtitle_inputs)):
            j, jtext, jfontsize = self.subtitle_inputs[i]
            jtext.set(folders[i])
                          
    # creates input areas and fontsize dropdowns based on length of data provided to histogram
    def makeSubtitleInputs(self):
        self.subtitle_inputs = []
        k = tk.Label(self.tabText,text="Plot Subtitles: ")
        k.grid(row=4, column=0, sticky="w", padx=(5,0), pady="5", columnspan=2)
        for i in range(self.subtitle_length):
            l = tk.Label(self.tabText, text=f"{i+1}: ")
            l.grid(row=i + 5, column=0, padx=(20,0), sticky="w")

            jtext = tk.StringVar(self)
            j = tk.Entry(self.tabText, textvariable=jtext)
            j.config(width=15)
            j.grid(row=i+5, column=1, sticky="w", padx=(0, 5), pady="5")

            jfont = [6, 7, 8, 9, 10, 11, 12]
            jvar = tk.IntVar(self)
            jvar.set(9)
            jfontwidget = tk.OptionMenu(self.tabText, jvar, *jfont)
            jfontwidget.grid(row=i+5, column=2)
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

    # generates a new pop up window to set the file path to save the figure at
    def savewindow(self):
        self.win = tk.Toplevel()
        self.win.title("Set Filepath: ")

        path = os.path.join(self.path, self.filename)

        s = ""
        savepath = path.split(".")
        if len(savepath) > 1:
            for path in savepath[:-1]:
                s+= path
        else:
            s = path
            
        #input area for file name, automatically sets to the filepath that was input originally
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
        self.qual_label.grid(row=  1, column=0)
        refqual = ["Low", "Medium", "High"]
        self.ref_qual = tk.StringVar(self)
        self.ref_qual.set('Medium')

        self.combo9 = tk.OptionMenu(self.win, self.ref_qual, *refqual)
        self.combo9.config(width=5)
        self.combo9.grid(row=1, column=1, sticky="w", padx=(0, 10), pady="10")

        # save button
        self.saveButton = tk.Button(self.win, text="SAVE", command=self.save)
        self.saveButton.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)
 
    # save histogram with matplotlib, close save window
    def save(self):
        self.hist.save(self.ref_path.get(), self.ref_type.get(), self.ref_qual.get())
        self.win.destroy()

    # alters the bin number/bin width input label based on whether bin number or width is toggled on
    def changeLabel(self):
            if self.bin1.get() == 1:
                self.bin_label.destroy()
                self.bin_label = tk.Label(self.tabFormat, text="Bins:")
                self.bin_label.grid(row=5, column=0, pady="5", padx=(20,0), sticky="w")
                self.bin2.set(0)

            elif self.bin1.get() == 0:
                self.bin_label.destroy()
                self.bin_label = tk.Label(self.tabFormat, text="Bins:")
                self.bin_label.grid(row=5, column=0, pady="5", padx=(20,0), sticky="w")
            else:
                self.bin_label.destroy()
                self.bin_label = tk.Label(self.tabFormat, text="Error! ")
                self.bin_label.grid(row=5, column=0, pady="5", padx=(20,0), sticky="w")

    # opens native color chooser dialog
    def choose_fillcolor(self):
        color_code, hexcode = colorchooser.askcolor(title="Choose Color")
        self.ref_color.set(hexcode)

    # opens native color chooser dialog
    def choose_edgecolor(self):
        color_code, hexcode = colorchooser.askcolor(title="Choose Color")
        self.ref_edgecolor.set(hexcode)

    # removes the last line from the histogram, if line edits are toggled on
    # - event: press of backspace key (optional)
    def undoLastLine(self, event=None):
        if self.linetoggle.get() == 1:
            if len(self.annotations) > 0:
                axis, x, y, dbl, color, style, lw = self.annotations.pop()
                
                # if dbl click line was added to entire figure, removes it as a single line
                while dbl:
                    axis, x, y, dbl, color, style, lw = self.annotations.pop()
                self.his()

    # opens native color chooser dialog
    def choose_linecolor(self):
        color_code, hexcode = colorchooser.askcolor(title="Choose Color")
        self.ref_linecolor.set(hexcode)

    # toggles bin number off and changes the label
    def togglebins(self):
        self.bin1.set(0)
        self.changeLabel()