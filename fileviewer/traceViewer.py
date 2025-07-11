import tkinter as tk
import glob
from fileviewer.fileViewerWindow import *
from traceReaderClass import *
import os

#/Users/katejackson/Desktop/Thrombin Aptamer/Apr15_11traces/(1) THROMBIN APTAMER, 0 mM KCl
#/Users/katejackson/Desktop/matlab_rec/

FILETYPE = '* tr*.dat' # not currently in use

# creates the trace viewing application as a tkinter toplevel
class TraceApplication(tk.Toplevel):

    def __init__(self):
        super().__init__()
        self.buildMenu()

    # builds the menu for inserting a file path in order to open trajectory files
    # trace files should be included in a single, accesible folder
    def buildMenu(self):
        self.title("View Traces")
        self.minsize(300, 200)

        # full window 
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)

        # start window
        self.subframe1 = tk.Frame(self.frame, background='white')
        self.subframe1.grid(row=0, column=0)

        # label
        self.title_label = tk.Label(self.subframe1, text="Open a .traces file:")
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=(10, 10), pady="10")

        # start button
        self.startButton = tk.Button(self.subframe1, text="START", command=self.onclick)
        self.startButton.grid(row=3, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)
        
        # input area for file path
        self.input_label = tk.Label(self.subframe1, text="Path:")
        self.input_label.grid(row=1, column=0)
        self.ref_input = tk.StringVar(self)
        self.ref_input.set('')

        self.combo4 = tk.Entry(self.subframe1, textvariable=self.ref_input)
        self.combo4.config(width=30)
        self.combo4.grid(row=1, column=1, sticky="ew", padx=(10, 10), pady="10")


    # when the start button is clicked, this function is run
    # processes input path to find data
    def onclick(self):
        keys = self.processPath2()
        trajectory_window = FileViewerWindow(self.ref_input.get(), keys)

    # initializes a TraceReader to parse the data in the file
    def processPath2(self):
        filepath = self.ref_input.get()
        reader = TraceReader(filepath)
        keys = reader.getData()
        return keys

    # finds all files of the designated file type within the folder specified by the user
    # not currently in use
    def processPath(self):
        filepath = self.ref_input.get() #creates variable from the file path set by the user
        filetype = FILETYPE #file type to look for
        keys = [] #empty list
        for root, dirs, files in os.walk(filepath): #for every file in the folder at the filepath
            dirs.sort() #sorts folders alphabetically
            files.sort() #sorts files alphabetically
            for file in files: #for every file in the path
                if glob.fnmatch.fnmatch(file, filetype): #if the file is of the correct filetype
                    keys.append(os.path.join(root, file)) #add the full file path to the list of keys
        return keys #return a list of filepaths, pointing to files of the correct file type
