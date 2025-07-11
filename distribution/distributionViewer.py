import tkinter as tk
import glob
from distribution.distributionWindow import *
import os

from traceReaderClass import TraceReader

#  ex file:   /Users/katejackson/Desktop/testdata

# when importing a folder, there shouldn't be any files in the folder other than trace files (dat or csv)
# files should contain data in three columns: time, donor, acceptor

FILETYPE = '* tr*.dat' #only relevant when importing dat files instead of csvs

# creates the FRET Efficiency distribution file builder as a tkinter toplevel
class DistApplication(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.buildMenu()

    # builds the menu for inserting a file path in order to open trajectory files
    # trace files should be included in a single, accesible folder
    def buildMenu(self):
        self.title("View Distribution")
        self.minsize(300, 200)

        #full window 
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)

        # start window
        self.subframe1 = tk.Frame(self.frame, background='white')
        self.subframe1.grid(row=0, column=0)

        # label
        self.title_label = tk.Label(self.subframe1, text="Open a folder containing traces or single trajectories:")
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=(10, 10), pady="10")

        #start button
        self.startButton = tk.Button(self.subframe1, text="START", command=self.onclick)
        self.startButton.grid(row=3, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)
        
        #input area for file path
        self.input_label = tk.Label(self.subframe1, text="Path:")
        self.input_label.grid(row=1, column=0)
        self.ref_input = tk.StringVar(self)
        self.ref_input.set('')

        self.combo4 = tk.Entry(self.subframe1, textvariable=self.ref_input)
        self.combo4.config(width=30)
        self.combo4.grid(row=1, column=1, sticky="ew", padx=(10, 10), pady="10")

        # dropdown for designation of filetype (either csv or dat)
        self.type_label = tk.Label(self.subframe1, text="File types:")
        self.type_label.grid(row=2, column=0)

        reftype = ['.csv', '.dat', '.traces']
        self.ref_type = tk.StringVar(self)
        self.ref_type.set('.traces')

        self.combo8 = tk.OptionMenu(self.subframe1, self.ref_type, *reftype)
        self.combo8.config(width=5)
        self.combo8.grid(row=2, column=1, sticky="ew", padx=(10, 10), pady="10")

    # when the start button is clicked, this function is run
    # finds all files of the correct file type and opens a new distribution window
    def onclick(self):
        if (self.ref_type.get() == ".csv"):
            keys = self.processPath() # individual file names
            filetype = 0
        elif (self.ref_type.get() == ".dat"):
            keys = self.processPath2() # individual file names
            filetype = 1
        elif (self.ref_type.get() == ".traces"):
            keys = self.processPath3() # list of dataframes
            filetype = 2
        distribution_window = DistributionWindow(self.ref_input.get(), keys, filetype)

    # finds all files of the designated file type within the folder specified by the user (CSV)
    def processPath(self):
        filepath = self.ref_input.get()
        extension = 'csv'
        os.chdir(filepath)
        keys = glob.glob('*.{}'.format(extension))
        return keys #individual file names, not full paths
    
    # finds all files of the designated file type within the folder specified by the user (DAT)
    def processPath2(self):
        filepath = self.ref_input.get()
        filetype = FILETYPE
        keys = []
        for root, dirs, files in os.walk(filepath):
            dirs.sort()
            files.sort()
            for file in files:
                if glob.fnmatch.fnmatch(file, filetype):
                    keys.append(file)
        return keys #individual file names, not full filepaths
    
    # initializes a TraceReader to parse the data from the file
    def processPath3(self):
        files = self.processPath4()
        print(f"traces files found: {len(files)}")
        path = self.ref_input.get()
        keys = []
        i = 0
        for file in files:
            name = os.path.join(path, file)
            print(f"file {i+1}: ")
            reader = TraceReader(name)
            keys += reader.getData()
            i+=1
        return keys
    
    def processPath4(self):
        filepath = self.ref_input.get()
        filetype = 'hel*.traces'
        keys = []
        for root, dirs, files in os.walk(filepath):
            dirs.sort()
            files.sort()
            for file in files:
                if glob.fnmatch.fnmatch(file, filetype):
                    keys.append(file)
        return keys #individual file names, not full filepaths
