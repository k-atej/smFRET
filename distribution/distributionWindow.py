import pandas as pd
import tkinter as tk
from distribution.distributionMaker import *

class DistributionWindow(tk.Toplevel):
    def __init__(self, path, files, filetype):
        super().__init__()
        self.minsize(200, 200)
        self.df = []
        self.path = path
        self.files = files # full file path
        self.distribution = None
        self.distribution2 = None
        self.filetype = filetype # 0 = csv, 1 = dat/fwf

        self.upper_limit = None
        self.lower_limit = None

        self.savepath = path.rstrip("/")
        #print(self.savepath)
        
        self.titleset = path.split("/")[-1] # final folder in the input path
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

    def start(self):
        self.makeButtons()
        self.makehist()
        self.bind('<Return>', self.makehist)

    
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


    # parses the data files into a pandas dataframe
    # needs to take frames 3 - 12 and average the FRET and intensity values for each (will need to calc E_FRET)
    # assemble all into one dataframe with a column for EFRET and a column for intensity (sum??)
    def get_data(self):
        all_data = pd.DataFrame(columns=["efret", "intensity"])

        for file in self.files:
            
            # open file
            filename = self.savepath + "/" + file
            newdata = open(filename, "r") 

            #get data into df
            if self.filetype == 0:
                data = pd.read_csv(newdata, header=None)
            elif self.filetype == 1:
                data = pd.read_fwf(newdata, header=None)
            
            data.columns = ["time", "donor", "acceptor"]
            data = data.iloc[3:13] #WANT TO CHANGE WHAT FRAMES ARE INCLUDED? CHANGE HERE!

            #calculate efret & intensity averages
            data["acceptor"] = data["acceptor"].astype(float)
            data["donor"] = data["donor"].astype(float)
            data['efret'] = data['acceptor'] / (data['acceptor'] + (data['donor']))
            data['intensity'] = data["acceptor"] + data['donor']
            average_e = data['efret'].mean()
            average_i = data['intensity'].mean()

            #transfer data to all_data
            newdat = {"efret": [average_e], "intensity": [average_i]}
            newdat_df = pd.DataFrame(newdat)
            all_data = pd.concat([newdat_df, all_data])

        self.df = all_data
        print(self.df)


    def makehist(self, event=None):        
        if self.distribution is not None:
            self.distribution.destroy()
        if self.distribution2 is not None:
            self.distribution2.destroy()
        self.get_data()


        self.distribution = DistributionMaker(self.df, "efret", self.path, self.subframeleft, 0, 0, self.upper_limit, self.lower_limit)
        self.distribution2 = DistributionMaker(self.df, "intensity", self.path, self.subframeleft, 1, 0, self.upper_limit, self.lower_limit)

    def setIntensity(self):
        self.win = tk.Toplevel()
        self.win.title("Set Cutoff Intensities:")

        self.upper_label = tk.Label(self.win, text="Set Upper Limit:")
        self.upper_label.grid(row=0, column=0, sticky="ew", padx="10", pady="10")

        self.ref_upper = tk.StringVar(self.win)
        #self.ref_upper.set() # set this to whatever the maximum intensity in the data is?
        self.upper = tk.Entry(self.win, textvariable=self.ref_upper)
        self.upper.config(width=25)
        self.upper.grid(row=0, column=1, sticky="ew", padx=(10, 20), pady="10")


        self.lower_label = tk.Label(self.win, text="Set Lower Limit:")
        self.lower_label.grid(row=1, column=0, sticky="ew", padx="10", pady="10")

        self.ref_lower = tk.StringVar(self.win)
        #self.ref_lower.set() # set this to whatever the maximum intensity in the data is?
        self.lower = tk.Entry(self.win, textvariable=self.ref_lower)
        self.lower.config(width=25)
        self.lower.grid(row=1, column=1, sticky="ew", padx=(10, 20), pady="10")

        self.setButton = tk.Button(self.win, text="SET CUTOFFS", command=self.setcutoff)
        self.setButton.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)

    def setcutoff(self):
        # get parameters
        self.upper_limit = self.ref_upper.get()
        self.lower_limit = self.ref_lower.get()

        self.makehist() # regenerate graph
        self.win.destroy() # close


    # this needs to be changed to suit however i am going to save this stuff
    def savewindow(self):
        self.win = tk.Toplevel()
        self.win.title("Set Filepath: ")
        
        #input area for file name
        self.path_label = tk.Label(self.win, text="Save File Path:")
        self.path_label.grid(row=0, column=0)
        self.ref_path = tk.StringVar(self.win)
        self.ref_path.set(self.savepath) # points to a folder

        self.combo6 = tk.Entry(self.win, textvariable=self.ref_path)
        self.combo6.config(width=50)
        self.combo6.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady="10")

        self.saveButton = tk.Button(self.win, text="SAVE", command=self.save)
        self.saveButton.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady="10", columnspan=2)



# this needs to be updated to save a .dat file that can be used for the graphing software
    def save(self):
        self.distribution.save(self.ref_path.get())
        self.win.destroy()

