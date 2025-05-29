import pandas as pd
import tkinter as tk
from distribution.distributionMaker import *
import os

SKIPPEDFRAMES = 2 # number of frames to skip at the beginning of each trace
INCLUDEDFRAMES = 10 # number of frames to include from each trace

# creates the window for making/viewing FRET Efficiency distribution files as a tkinter toplevel
class DistributionWindow(tk.Toplevel):

    # initializes the window for viewing files
    #   - path: user input filepath
    #   - files: keys, individual file names found in designated folder
    #   - filetype: .csv (0) or .dat (1)
    def __init__(self, path, files, filetype): #path = user input, files = keys, filetype = csv or dat
        super().__init__()
        self.minsize(200, 200)
        self.df = []

        # individual file names, not full file paths
        self.files = files 
        self.filetype = filetype

        # set parameters for future generations of distributino
        self.distribution = None
        self.distribution2 = None
        self.upper_limit = None
        self.lower_limit = None

        # processing the user input to set the save path and the window title
        self.savepath = path.rstrip("\\/")
        self.titleset = os.path.basename(self.savepath) 
        self.title(self.titleset)

        #full window 
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0)

        #area above the intensity viewer
        self.subframetop = tk.Frame(self.frame, background='white')
        self.subframetop.grid(row=0, column=0, columnspan=2)

        # left half (contains intensities and efret figures)
        self.subframeleft = tk.Frame(self.frame, background='white')
        self.subframeleft.grid(row=1, column=0, padx=(20, 0))

        # right half (contains menu)
        self.subframeright = tk.Frame(self.frame, background='white')
        self.subframeright.grid(row=1, column=1)

        self.start()

    # pastes the buttons/options onto the window and creates the trajectory
    # binds keys to various functions
    def start(self):
        self.makeButtons()
        self.makehist()
        self.bind('<Return>', self.makehist)

    # pastes the buttons/options onto the window and creates the trajectory 
    def makeButtons(self):
        # generate button, bound to the generation of a histogram
        makeTraj = tk.Button(self.subframetop, text="Generate", command=self.makehist)
        makeTraj.grid(row=0, column=2, padx="10")
    
        # save button
        self.saveButton = tk.Button(self.subframetop, text="Save", command=self.savewindow)
        self.saveButton.grid(row=0, column=3, sticky="ew", padx="10", pady="10")

        # set intensities button
        self.intensityButton = tk.Button(self.subframetop, text="Set Intensity Cutoff", command=self.setIntensity)
        self.intensityButton.grid(row=0, column=4, sticky="ew", padx="10", pady="10")


    # parses the data files into a pandas dataframe by taking a certain number of frames from the beginning
    def get_data(self):
        all_data = pd.DataFrame(columns=["efret", "intensity"])

        for file in self.files:
            # open file
            filename = os.path.join(self.savepath, file)
            newdata = open(filename, "r") 

            #get data into a dataframe
            if self.filetype == 0:
                data = pd.read_csv(newdata, header=None)
            elif self.filetype == 1:
                data = pd.read_fwf(newdata, header=None)
            
            # select only the desired frames from the beginning of the trace
            startframe = SKIPPEDFRAMES + 1
            endframe = startframe + INCLUDEDFRAMES
            data.columns = ["time", "donor", "acceptor"]
            data = data.iloc[startframe:endframe] 

            #calculate FRET efficiency & intensity averages
            data["acceptor"] = data["acceptor"].astype(float)
            data["donor"] = data["donor"].astype(float)
            data['efret'] = data['acceptor'] / (data['acceptor'] + (data['donor']))
            data['intensity'] = data["acceptor"] + data['donor']
            average_e = data['efret'].mean()
            average_i = data['intensity'].mean()

            #transfer data to all_data dataframe
            newdat = {"efret": [average_e], "intensity": [average_i]}
            newdat_df = pd.DataFrame(newdat)
            all_data = pd.concat([newdat_df, all_data])

        self.df = all_data

    def makehist(self, event=None):
        # remove any previous data        
        if self.distribution is not None:
            self.distribution.destroy()
        if self.distribution2 is not None:
            self.distribution2.destroy()
        
        #retrieve data from files
        self.get_data()

        # make the FRET efficiency distribution histogram
        self.distribution = DistributionMaker(self.df, "efret", self.savepath, self.subframeleft, 0, 
                                              0, self.upper_limit, self.lower_limit)
        # make the fluorophore intensity distribution histogram
        self.distribution2 = DistributionMaker(self.df, "intensity", self.savepath, self.subframeleft, 1,
                                               0, self.upper_limit, self.lower_limit)

    # creates a new window for setting upper and lower fluorophore intensity cutoffs
    def setIntensity(self):
        self.win = tk.Toplevel()
        self.win.title("Set Cutoff Intensities:")

        # upper bound
        self.upper_label = tk.Label(self.win, text="Set Upper Limit:")
        self.upper_label.grid(row=0, column=0, sticky="ew", padx="10", pady="10")

        self.ref_upper = tk.StringVar(self.win)
        self.upper = tk.Entry(self.win, textvariable=self.ref_upper)
        self.upper.config(width=25)
        self.upper.grid(row=0, column=1, sticky="ew", padx=(10, 20), pady="10")

        # lower bound
        self.lower_label = tk.Label(self.win, text="Set Lower Limit:")
        self.lower_label.grid(row=1, column=0, sticky="ew", padx="10", pady="10")

        self.ref_lower = tk.StringVar(self.win)
        self.lower = tk.Entry(self.win, textvariable=self.ref_lower)
        self.lower.config(width=25)
        self.lower.grid(row=1, column=1, sticky="ew", padx=(10, 20), pady="10")

        # set cutoffs button
        self.setButton = tk.Button(self.win, text="SET CUTOFFS", command=self.setcutoff)
        self.setButton.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)

    # saves the intensity cutoffs & regenerates the histograms accordingly
    # closes cutoff window
    def setcutoff(self):
        self.upper_limit = self.ref_upper.get()
        self.lower_limit = self.ref_lower.get()
        self.makehist() 
        self.win.destroy()

    # creates a small window for user to enter the path to save the FRET efficiency file to
    # user input should be a folder
    # user can save distribution file as a csv or dat 
    def savewindow(self):
        self.win = tk.Toplevel()
        self.win.title("Set Filepath: ")
        
        #input area for file name
        self.path_label = tk.Label(self.win, text="Save File Path:")
        self.path_label.grid(row=0, column=0)
        self.ref_path = tk.StringVar(self.win)
        self.ref_path.set(self.savepath)

        self.combo6 = tk.Entry(self.win, textvariable=self.ref_path)
        self.combo6.config(width=50)
        self.combo6.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady="10")

        # dropdown for designation of filetype (either csv or dat)
        self.type_label = tk.Label(self.win, text="File Types:")
        self.type_label.grid(row=2, column=0)

        reftype = ['.csv', '.dat']
        self.ref_type = tk.StringVar(self)
        self.ref_type.set('.csv')

        self.combo8 = tk.OptionMenu(self.win, self.ref_type, *reftype)
        self.combo8.config(width=5)
        self.combo8.grid(row=2, column=1, sticky="ew", padx=(10, 10), pady="10")

        # save button
        self.saveButton = tk.Button(self.win, text="SAVE", command=self.save)
        self.saveButton.grid(row=3, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)

    # saves the distribution file to the given file path
    def save(self):
        self.distribution.save(self.ref_path.get(), self.ref_type.get())
        self.win.destroy()

