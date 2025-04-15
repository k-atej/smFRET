import tkinter as tk
import glob
from distributionWindow import *
import os

#  ex file:   /Users/katejackson/Desktop/testdata

# TO DO:
    # make small pop up window to set high and low cutoff intensities?
    # save file to FRETResult.dat
    # generalize file opener to also work with regular trace file types (specify when entering file path?)

# initializes and runs the application
def main():
    app = Application()
    app.mainloop()


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.buildMenu()

    def buildMenu(self):
        self.title("Open Folder of Trajectory Files")
        self.minsize(300, 200)

        #full window 
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)

        # start window
        self.subframe1 = tk.Frame(self.frame, background='white')
        self.subframe1.grid(row=0, column=0)

        #Title
        self.title_label = tk.Label(self.subframe1, text="Open A Folder:")
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=(10, 10), pady="10")

        #start button
        self.startButton = tk.Button(self.subframe1, text="START", command=self.onclick)
        self.startButton.grid(row=3, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)
        
        #input area for file path
        self.input_label = tk.Label(self.subframe1, text="File Path:")
        self.input_label.grid(row=1, column=0)
        self.ref_input = tk.StringVar(self)
        self.ref_input.set('')

        self.combo4 = tk.Entry(self.subframe1, textvariable=self.ref_input)
        self.combo4.config(width=30)
        self.combo4.grid(row=1, column=1, sticky="ew", padx=(10, 10), pady="10")


    def onclick(self):
        keys = self.processPath()
        print(f"csv files found: {keys}")
        distribution_window = DistributionWindow(self.ref_input.get(), keys)


    def processPath(self):
        filepath = self.ref_input.get()
        extension = 'csv'
        os.chdir(filepath)
        keys = glob.glob('*.{}'.format(extension))

        return keys





main()