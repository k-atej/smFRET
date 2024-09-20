import pandas as pd
import tkinter as tk
from matplotlib.figure import Figure
from histogramMaker import *
from tableMaker import *


def main():
    data =  {'time': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'donor': [2, 4, 6, 8, 4, 1, 3, 9, 2, 5], 'acceptor': [3, 6, 9, 12, 3, 2, 4, 5, 3, 2]}
    df = pd.DataFrame(data=data)
    app = Application(df)
    app.mainloop()

class Application(tk.Tk):

    def __init__(self, df):
        super().__init__()
        self.title("Test")
        self.minsize(200, 200)
        self.df = df
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)

        self.subframe1 = tk.Frame(self.frame, background='white')
        self.subframe1.grid(row=0, column=0)

        self.subframeright = tk.Frame(self.frame, background='white')
        self.subframeright.grid(row=0, column=1)

        self.subframe2 = tk.Frame(self.subframeright, background='white')
        self.subframe2.grid(row=0, column=0)

        self.subframe3 = tk.Frame(self.subframeright, background='white')
        self.subframe3.grid(row=1, column=0)
        
        self.startButton = tk.Button(self.subframe1, text="start", command=self.start)
        self.startButton.grid(row=1, column=1)
        #where did this button go? 

    def start(self):
        self.startButton.destroy()

        efretCalculator(self.df)
        self.table()
        self.makeFeatures()

    def makeFeatures(self):
        self.makeButtons()
        self.makeOptions()

    def makeButtons(self):
        makeHist = tk.Button(self.subframe1, text="Make Histogram from:", command=self.his)
        makeHist.grid(row=1, column=0)

        self.clearButton = tk.Button(self.subframe3, text="Clear", command=self.emptyHis)
        self.clearButton.grid(row=0, column=0, sticky="ew", padx="100", pady="20")
        
    def makeOptions(self):
        labels = self.df.columns
        self.ref_col = tk.StringVar(self)
        self.ref_col.set("Reference Column")

        self.combo = tk.OptionMenu(self.subframe1, self.ref_col, *labels)
        self.combo.config(width=20)
        self.combo.grid(row=2, column=0)



        self.bin_label = tk.Label(self.subframe3, text="Bins:")
        self.bin_label.grid(row=0, column=1)
        self.ref_bins = tk.StringVar(self)
        self.ref_bins.set("10")

        self.combo = tk.Entry(self.subframe3, textvariable=self.ref_bins)
        self.combo.config(width=20)
        self.combo.grid(row=0, column=2, sticky="ew", padx=(0, 100), pady="20")
    
    def table(self): # i may want to turn this into a class
        makeTable(self.df, self.subframe1, 0, 0)
        self.emptyHis()
    
    def emptyHis(self):
        emptyHistogram(self.subframe2, 0, 0)

    def his(self): #creates histogram from sample data
        col = self.ref_col.get()
        bins = int(self.ref_bins.get())
        if col == "Reference Column":
            pass
        else:
            print(col)
            makeHistogram(self.df[col], self.subframe2, 0, 0, bins)

    def emptyFig(self):
        fig = Figure()
        canvas = FigureCanvasTkAgg(fig, master=self.subframe2)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1)
        
if __name__ == "__main__":
    main()