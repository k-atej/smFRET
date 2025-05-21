import tkinter as tk
import glob
from distribution.distributionWindow import *
import os

#  ex file:   /Users/katejackson/Desktop/testdata



class DistApplication(tk.Toplevel):

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

        # dropdown for designation of filetype
        self.type_label = tk.Label(self.subframe1, text="File Types:")
        self.type_label.grid(row=2, column=0)

        reftype = ['.csv', '.dat']
        self.ref_type = tk.StringVar(self)
        self.ref_type.set('.csv')

        self.combo8 = tk.OptionMenu(self.subframe1, self.ref_type, *reftype)
        self.combo8.config(width=5)
        self.combo8.grid(row=2, column=1, sticky="ew", padx=(10, 10), pady="10")


    def onclick(self):
        if (self.ref_type.get() == ".csv"):
            keys = self.processPath()
            filetype = 0
        elif (self.ref_type.get() == ".dat"):
            keys = self.processPath2()
            filetype = 1
        #print(f"csv files found: {keys}")
        distribution_window = DistributionWindow(self.ref_input.get(), keys, filetype)


    def processPath(self):
        filepath = self.ref_input.get()
        extension = 'csv'
        os.chdir(filepath)
        keys = glob.glob('*.{}'.format(extension))

        return keys
    
    def processPath2(self):
        filepath = self.ref_input.get()
        #print(filepath)
        filetype = '* tr*.dat'
        keys = []
        for root, dirs, files in os.walk(filepath):
            dirs.sort()
            files.sort()
            for file in files:
                if glob.fnmatch.fnmatch(file, filetype):
                    keys.append(file)
                    #keys.append(os.path.join(root, file))
        return keys
