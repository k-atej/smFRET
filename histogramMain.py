import tkinter as tk
from histogramMaker import *
from histogramWindow import *
from stackedHistogramWindow import *
import os

#file name to look for results in, should probably be able to change this
eFRET_FILE_NAME = "FRETresult.dat"

#example MacOS filepath
path = "/Users/katejackson/Desktop/Thrombin Aptamer/Apr15_11 copy"


# opens a small window. takes a file path and decides whether to open a histogram or stacked histogram window based on the number of eFRET_FILE_NAMEs found. 
class HistogramMainApplication(tk.Toplevel):

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

        #start button
        self.startButton = tk.Button(self.subframe1, text="START", command=self.start)
        self.startButton.grid(row=3, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)
        
        #input area for file path
        self.input_label = tk.Label(self.subframe1, text="File Path:")
        self.input_label.grid(row=1, column=0)
        self.ref_input = tk.StringVar(self)
        self.ref_input.set('')

        self.combo4 = tk.Entry(self.subframe1, textvariable=self.ref_input)
        self.combo4.config(width=30)
        self.combo4.grid(row=1, column=1, sticky="ew", padx=(10, 10), pady="10")

        #input area for file name
        self.file_label = tk.Label(self.subframe1, text="Data File Name:")
        self.file_label.grid(row=2, column=0)
        self.ref_file = tk.StringVar(self)
        self.ref_file.set('FRETresult.dat')

        self.combo4 = tk.Entry(self.subframe1, textvariable=self.ref_file)
        self.combo4.config(width=30)
        self.combo4.grid(row=2, column=1, sticky="ew", padx=(10, 10), pady="10")

    # walks through folders in the file path and identifies that number of eFRET_FILE_NAMEs present. decides whether a single or stacked histogram is appropriate,
    # and opens the corresponding window. 
    def start(self):
        self.path = self.ref_input.get()
        keys = []
        for root, dirs, files in os.walk(self.path):
               for file in files:
                if file.endswith(self.ref_file.get()):
                    keys.append(file)
        if len(keys) == 1:
            histapp = HistApplication(self.path, self.ref_file.get(), self.getTitle())
            #histapp.mainloop()
        elif len(keys) > 1:
            stackedhistapp = StackedHistApplication(self.path, self.ref_file.get(), self.getTitle())
            #stackedhistapp.mainloop()

    #returns the name of the final folder in the file path, to set as the window title
    def getTitle(self):
        path = self.path.split("/")
        title = path[-1]
        return title


        
#if __name__ == "__main__":
 #   main()