import pandas as pd
import numpy as np
import tkinter as tk

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
        self.title("Testing Again")
        self.minsize(200, 200)
        self.df = df
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)
        
        self.startButton = tk.Button(self, text="start", command=self.start)
        self.startButton.grid(row=1, column=1)
        #where did this button go? 

    def start(self):
        self.startButton.destroy()
        makeHist = tk.Button(self, text="Make Histogram from eFRET", command=self.his)
        makeHist.grid(row=1, column=0)

        efretCalculator(self.df)
        self.table()
        
    def table(self): # i may want to turn this into a class
        makeTable(self.df, self.frame, 0, 0)
    
    def his(self): #creates histogram from sample data
        makeHistogram(self.df["eFRET"], self.frame, 0, 1)
        
if __name__ == "__main__":
    main()