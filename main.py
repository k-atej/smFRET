import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from histogramMaker import *
from tableMaker import *
from tkinter.filedialog import askopenfile

#file name
eFRET_FILE_NAME = "FRETresult.dat"

#MacOS filepath
path = "/Users/katejackson/Desktop/Thrombin Aptamer/Apr15_11/(1) THROMBIN APTAMER, 0 mM KCl"

def main():
    data =  {'time': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'donor': [2, 4, 6, 8, 4, 1, 3, 9, 2, 5], 'acceptor': [3, 6, 9, 12, 3, 2, 4, 5, 3, 2]}
    df = pd.DataFrame(data=data)
    app = Application(df)
    app.mainloop()

class Application(tk.Tk):

    def __init__(self, df):
        super().__init__()
        self.title("Histogram Maker")
        self.minsize(200, 200)
        self.df = df

        #full window 
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)

        # start window
        self.subframe1 = tk.Frame(self.frame, background='white')
        self.subframe1.grid(row=0, column=0)

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
        
        #placeholder button
        self.startButton = tk.Button(self.subframe1, text="start", command=self.start)
        self.startButton.grid(row=0, column=0)
        #where did this button go? 

        self.input_label = tk.Label(self.subframe1, text="File Path:")
        self.input_label.grid(row=1, column=0)
        self.ref_input = tk.StringVar(self)
        self.ref_input.set('')

        self.combo4 = tk.Entry(self.subframe1, textvariable=self.ref_input)
        self.combo4.config(width=30)
        self.combo4.grid(row=1, column=3, sticky="ew", padx=(0, 10), pady="10")


    def get_data(self, path):
        FRETresult = open(path + "/" + eFRET_FILE_NAME, "r") 
        data = pd.read_fwf(FRETresult, header=None)
        data.columns = ["eFRET", "other"]
        self.df = data

    def start(self):

        self.path = self.ref_input.get()
        self.get_data(self.path)

        self.startButton.destroy()
        self.input_label.destroy()
        self.combo4.destroy()
        self.subframe1.destroy()
        #efretCalculator(self.df)
        #self.table()
        self.emptyHis()
        self.makeFeatures()

    def makeFeatures(self):
        self.makeFormat()
        self.makeOptions()
        self.makeButtons()
        self.bind('<Return>', self.his)

    def makeFormat(self):
        self.tabControl = ttk.Notebook(master=self.window1)
        self.tabFormat = tk.Frame(self.tabControl)
        self.tabStyle = tk.Frame(self.tabControl)
        self.tabText = tk.Frame(self.tabControl)

        self.tabControl.add(self.tabFormat, text="Format")
        self.tabControl.add(self.tabStyle, text="Style")
        self.tabControl.add(self.tabText, text="Text")
        self.tabControl.grid(row=0, column=0, rowspan=3, padx=10)

    def makeButtons(self):
        makeHist = tk.Button(self.subframe3, text="Generate", command=self.his)
        makeHist.grid(row=0, column=0, padx="10")

        self.clearButton = tk.Button(self.subframe3, text="Clear", command=self.emptyHis)
        self.clearButton.grid(row=0, column=2, sticky="ew", padx="10", pady="10")

    def makeOptions(self):
        self.lbl_label = tk.Label(self.tabFormat, text="Data Column:")
        self.lbl_label.grid(row=0, column=0)
        labels = self.df.columns
        self.ref_col = tk.StringVar(self)
        self.ref_col.set("eFRET")

        self.combo = tk.OptionMenu(self.tabFormat, self.ref_col, *labels)
        self.combo.config(width=10)
        self.combo.grid(row=0, column=1)

        self.bin_label = tk.Label(self.tabFormat, text="Bins:")
        self.bin_label.grid(row=1, column=0)
        self.ref_bins = tk.StringVar(self)
        self.ref_bins.set("Auto")

        self.combo1 = tk.Entry(self.tabFormat, textvariable=self.ref_bins)
        self.combo1.config(width=10)
        self.combo1.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="10")

        self.offset_label = tk.Label(self.tabFormat, text="Offset:")
        self.offset_label.grid(row=1, column=2)
        self.ref_offset = tk.StringVar(self)
        self.ref_offset.set('0.0')

        self.combo3 = tk.Entry(self.tabFormat, textvariable=self.ref_offset)
        self.combo3.config(width=10)
        self.combo3.grid(row=1, column=3, sticky="ew", padx=(0, 10), pady="10")


        self.xmax_label = tk.Label(self.tabFormat, text="X Max:")
        self.xmax_label.grid(row=0, column=4)
        self.ref_xmax = tk.StringVar(self)
        self.ref_xmax.set('None')

        self.comboxmax = tk.Entry(self.tabFormat, textvariable=self.ref_xmax)
        self.comboxmax.config(width=5)
        self.comboxmax.grid(row=0, column=5, sticky="ew", padx=(0, 10), pady="10")

        self.xmin_label = tk.Label(self.tabFormat, text="X Min:")
        self.xmin_label.grid(row=1, column=4)
        self.ref_xmin = tk.StringVar(self)
        self.ref_xmin.set('None')

        self.comboxmin = tk.Entry(self.tabFormat, textvariable=self.ref_xmin)
        self.comboxmin.config(width=5)
        self.comboxmin.grid(row=1, column=5, sticky="ew", padx=(0, 10), pady="10")


        self.ymax_label = tk.Label(self.tabFormat, text="Y Max:")
        self.ymax_label.grid(row=0, column=6)
        self.ref_ymax = tk.StringVar(self)
        self.ref_ymax.set('None')

        self.comboymax = tk.Entry(self.tabFormat, textvariable=self.ref_ymax)
        self.comboymax.config(width=5)
        self.comboymax.grid(row=0, column=7, sticky="ew", padx=(0, 10), pady="10")

        self.ymin_label = tk.Label(self.tabFormat, text="Y Min:")
        self.ymin_label.grid(row=1, column=6)
        self.ref_ymin = tk.StringVar(self)
        self.ref_ymin.set('None')

        self.comboymin = tk.Entry(self.tabFormat, textvariable=self.ref_ymin)
        self.comboymin.config(width=5)
        self.comboymin.grid(row=1, column=7, sticky="ew", padx=(0, 10), pady="10")



        # second tab = style


        self.title_label = tk.Label(self.tabText, text="Title:")
        self.title_label.grid(row=0, column=0)
        self.ref_title = tk.StringVar(self)
        self.ref_title.set("Title")

        self.combo2 = tk.Entry(self.tabText, textvariable=self.ref_title)
        self.combo2.config(width=10)
        self.combo2.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady="10")


        self.x_label = tk.Label(self.tabText, text="X-Axis Label:")
        self.x_label.grid(row=0, column=2)
        self.ref_x = tk.StringVar(self)
        self.ref_x.set("X-Axis")

        self.combo2 = tk.Entry(self.tabText, textvariable=self.ref_x)
        self.combo2.config(width=10)
        self.combo2.grid(row=0, column=3, sticky="ew", padx=(0, 10), pady="10")

        self.y_label = tk.Label(self.tabText, text="Y-Axis Label:")
        self.y_label.grid(row=0, column=4)
        self.ref_y = tk.StringVar(self)
        self.ref_y.set("Y-Axis")

        self.combo2 = tk.Entry(self.tabText, textvariable=self.ref_y)
        self.combo2.config(width=10)
        self.combo2.grid(row=0, column=5, sticky="ew", padx=(0, 10), pady="10")

        self.color_label = tk.Label(self.tabStyle, text="Color:")
        self.color_label.grid(row=1, column=0)
        self.ref_color = tk.StringVar(self)
        self.ref_color.set("0")

        self.combo2 = tk.Entry(self.tabStyle, textvariable=self.ref_color)
        self.combo2.config(width=10)
        self.combo2.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="10")

        self.edgecolor_label = tk.Label(self.tabStyle, text="Edge Color:")
        self.edgecolor_label.grid(row=1, column=2)
        self.ref_edgecolor = tk.StringVar(self)
        self.ref_edgecolor.set("0")

        self.combo5 = tk.Entry(self.tabStyle, textvariable=self.ref_edgecolor)
        self.combo5.config(width=10)
        self.combo5.grid(row=1, column=3, sticky="ew", padx=(0, 10), pady="10")

        self.edgewidth_label = tk.Label(self.tabStyle, text="Edge Width:")
        self.edgewidth_label.grid(row=1, column=4)
        self.ref_edgewidth = tk.StringVar(self)
        self.ref_edgewidth.set("1")

        self.combo6 = tk.Entry(self.tabStyle, textvariable=self.ref_edgewidth)
        self.combo6.config(width=10)
        self.combo6.grid(row=1, column=5, sticky="ew", padx=(0, 10), pady="10")

        self.xfontsize_label = tk.Label(self.tabText, text="X Font Size:")
        self.xfontsize_label.grid(row=0, column=6)
        self.ref_xfontsize = tk.StringVar(self)
        self.ref_xfontsize.set("10")

        self.combo7 = tk.Entry(self.tabText, textvariable=self.ref_xfontsize)
        self.combo7.config(width=10)
        self.combo7.grid(row=0, column=7, sticky="ew", padx=(0, 10), pady="10")

        self.yfontsize_label = tk.Label(self.tabText, text="Y Font Size:")
        self.yfontsize_label.grid(row=1, column=6)
        self.ref_yfontsize = tk.StringVar(self)
        self.ref_yfontsize.set("10")

        self.combo8 = tk.Entry(self.tabText, textvariable=self.ref_yfontsize)
        self.combo8.config(width=10)
        self.combo8.grid(row=1, column=7, sticky="ew", padx=(0, 10), pady="10")

    def table(self): # i may want to turn this into a class
        makeTable(self.df, self.subframe1, 0, 0)
    
    def emptyHis(self):
        emptyHistogram(self.subframe2, 0, 0)

    def his(self, event=None): #creates histogram from sample data
        col = self.ref_col.get()
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

        xfontsize = float(self.ref_xfontsize.get())
        yfontsize = float(self.ref_yfontsize.get())
        bin_num = makeHistogram(self.df[col], self.subframe2, 0, 0, bins, title, x_ax, y_ax, color, edgecolor, edgewidth, xmax, xmin, ymax, ymin, xfontsize, yfontsize, offset)
        self.ref_bins.set(bin_num)

    def checkMinMax(self, val):
        if val != 'None':
            val = float(val)
        else:
            val = None
        return val
    
    def emptyFig(self):
        fig = Figure()
        canvas = FigureCanvasTkAgg(fig, master=self.subframe2)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1)
        
if __name__ == "__main__":
    main()