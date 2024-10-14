import pandas as pd
import tkinter as tk
from histogramMaker import *
from tableMaker import *
from histogramwindow import *

#file name
eFRET_FILE_NAME = "FRETresult.dat"

#MacOS filepath
path = "/Users/katejackson/Desktop/Thrombin Aptamer/Apr15_11/(1) THROMBIN APTAMER, 0 mM KCl"

def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Histogram Maker")
        self.minsize(200, 200)
        self.df = []

        #full window 
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)

        # start window
        self.subframe1 = tk.Frame(self.frame, background='white')
        self.subframe1.grid(row=0, column=0)

        #Title
        self.title_label = tk.Label(self.subframe1, text="Open A File:")
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=(10, 10), pady="10")

        #placeholder button
        self.startButton = tk.Button(self.subframe1, text="start", command=self.start)
        self.startButton.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)
        
        #where did this button go? 
        self.input_label = tk.Label(self.subframe1, text="File Path:")
        self.input_label.grid(row=1, column=0)
        self.ref_input = tk.StringVar(self)
        self.ref_input.set('')

        self.combo4 = tk.Entry(self.subframe1, textvariable=self.ref_input)
        self.combo4.config(width=30)
        self.combo4.grid(row=1, column=1, sticky="ew", padx=(10, 10), pady="10")


    def get_data(self, path):
        FRETresult = open(path + "/" + eFRET_FILE_NAME, "r") 
        data = pd.read_fwf(FRETresult, header=None)
        data.columns = ["eFRET", "other"]
        self.df = data

    def start(self):
        self.path = self.ref_input.get()
        self.get_data(self.path)
        histapp = HistApplication(self.df, self.getTitle())
        histapp.mainloop()
    
    def getTitle(self):
        path = self.path.split("/")
        title = path[-1]
        return title


        
if __name__ == "__main__":
    main()