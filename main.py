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

        # left half of window
        self.subframe1 = tk.Frame(self.frame, background='white')
        self.subframe1.grid(row=0, column=0)

        # right half of window
        self.subframeright = tk.Frame(self.frame, background='white')
        self.subframeright.grid(row=0, column=1)

        # upper half of subframeright
        self.subframe2 = tk.Frame(self.subframeright, background='white')
        self.subframe2.grid(row=0, column=0)
        
        # lower half of subframeright
        self.subframe3 = tk.Frame(self.subframeright, background='white')
        self.subframe3.grid(row=1, column=0)
        
        #placeholder button
        self.startButton = tk.Button(self.subframe1, text="start", command=self.start)
        self.startButton.grid(row=0, column=0)
        #where did this button go? 

        self.input_label = tk.Label(self.subframe1, text="File Path:")
        self.input_label.grid(row=1, column=0)
        self.ref_input = tk.StringVar(self)
        self.ref_input.set('None')

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
        self.tabControl = ttk.Notebook(master=self.subframe3)
        self.tab1 = tk.Frame(self.tabControl)
        self.tab2 = tk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text="Format")
        self.tabControl.add(self.tab2, text="Style")
        self.tabControl.grid(row=0, column=0, padx=10)

    def makeButtons(self):
        makeHist = tk.Button(self.tab1, text="Generate from:", command=self.his)
        makeHist.grid(row=0, column=0, padx="10")

        self.clearButton = tk.Button(self.tab1, text="Clear", command=self.emptyHis)
        self.clearButton.grid(row=0, column=2, sticky="ew", padx="10", pady="10")

    def makeOptions(self):
        labels = self.df.columns
        self.ref_col = tk.StringVar(self)
        self.ref_col.set("eFRET")

        self.combo = tk.OptionMenu(self.tab1, self.ref_col, *labels)
        self.combo.config(width=20)
        self.combo.grid(row=0, column=1)

        self.bin_label = tk.Label(self.tab1, text="Bins:")
        self.bin_label.grid(row=1, column=0)
        self.ref_bins = tk.StringVar(self)
        self.ref_bins.set("Auto")

        self.combo1 = tk.Entry(self.tab1, textvariable=self.ref_bins)
        self.combo1.config(width=10)
        self.combo1.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="10")

        self.offset_label = tk.Label(self.tab1, text="Offset:")
        self.offset_label.grid(row=1, column=2)
        self.ref_offset = tk.StringVar(self)
        self.ref_offset.set('0.0')

        self.combo3 = tk.Entry(self.tab1, textvariable=self.ref_offset)
        self.combo3.config(width=10)
        self.combo3.grid(row=1, column=3, sticky="ew", padx=(0, 10), pady="10")


        self.xmax_label = tk.Label(self.tab1, text="X Max:")
        self.xmax_label.grid(row=0, column=4)
        self.ref_xmax = tk.StringVar(self)
        self.ref_xmax.set('1.0')

        self.comboxmax = tk.Entry(self.tab1, textvariable=self.ref_xmax)
        self.comboxmax.config(width=5)
        self.comboxmax.grid(row=0, column=5, sticky="ew", padx=(0, 10), pady="10")

        self.xmin_label = tk.Label(self.tab1, text="X Min:")
        self.xmin_label.grid(row=1, column=4)
        self.ref_xmin = tk.StringVar(self)
        self.ref_xmin.set('0.0')

        self.comboxmin = tk.Entry(self.tab1, textvariable=self.ref_xmin)
        self.comboxmin.config(width=5)
        self.comboxmin.grid(row=1, column=5, sticky="ew", padx=(0, 10), pady="10")



        # second tab = style


        self.title_label = tk.Label(self.tab2, text="Title:")
        self.title_label.grid(row=0, column=0)
        self.ref_title = tk.StringVar(self)
        self.ref_title.set("Title")

        self.combo2 = tk.Entry(self.tab2, textvariable=self.ref_title)
        self.combo2.config(width=10)
        self.combo2.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady="10")


        self.x_label = tk.Label(self.tab2, text="X-Axis Label:")
        self.x_label.grid(row=0, column=2)
        self.ref_x = tk.StringVar(self)
        self.ref_x.set("X-Axis")

        self.combo2 = tk.Entry(self.tab2, textvariable=self.ref_x)
        self.combo2.config(width=10)
        self.combo2.grid(row=0, column=3, sticky="ew", padx=(0, 10), pady="10")

        self.y_label = tk.Label(self.tab2, text="Y-Axis Label:")
        self.y_label.grid(row=0, column=4)
        self.ref_y = tk.StringVar(self)
        self.ref_y.set("Y-Axis")

        self.combo2 = tk.Entry(self.tab2, textvariable=self.ref_y)
        self.combo2.config(width=10)
        self.combo2.grid(row=0, column=5, sticky="ew", padx=(0, 10), pady="10")

        self.color_label = tk.Label(self.tab2, text="Color:")
        self.color_label.grid(row=1, column=0)
        self.ref_color = tk.StringVar(self)
        self.ref_color.set("0")

        self.combo2 = tk.Entry(self.tab2, textvariable=self.ref_color)
        self.combo2.config(width=10)
        self.combo2.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady="10")

        self.edgecolor_label = tk.Label(self.tab2, text="Edge Color:")
        self.edgecolor_label.grid(row=1, column=2)
        self.ref_edgecolor = tk.StringVar(self)
        self.ref_edgecolor.set("0")

        self.combo5 = tk.Entry(self.tab2, textvariable=self.ref_edgecolor)
        self.combo5.config(width=10)
        self.combo5.grid(row=1, column=3, sticky="ew", padx=(0, 10), pady="10")

        self.edgewidth_label = tk.Label(self.tab2, text="Edge Width:")
        self.edgewidth_label.grid(row=1, column=4)
        self.ref_edgewidth = tk.StringVar(self)
        self.ref_edgewidth.set("1")

        self.combo6 = tk.Entry(self.tab2, textvariable=self.ref_edgewidth)
        self.combo6.config(width=10)
        self.combo6.grid(row=1, column=5, sticky="ew", padx=(0, 10), pady="10")

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
        xmax = float(self.ref_xmax.get())
        xmin = float(self.ref_xmin.get())
        bin_num = makeHistogram(self.df[col], self.subframe2, 0, 0, bins, title, x_ax, y_ax, color, edgecolor, edgewidth, xmax, xmin, offset)
        self.ref_bins.set(bin_num)

    def emptyFig(self):
        fig = Figure()
        canvas = FigureCanvasTkAgg(fig, master=self.subframe2)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1)
        
if __name__ == "__main__":
    main()