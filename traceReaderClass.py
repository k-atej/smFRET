import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# adapted from the traceReader
# parses data from the .traces files and returns a list of dataframes that have been smoothed + filtered

TIME = 0.1 # time resolution
WINDOW = 3 # rolling average window size
THRESHOLD = 6000


class TraceReader():
    def __init__(self, path):
        self.path = path
        self.dfs = self.parse()
        self.filtereddfs = []

        for df in self.dfs:
            self.filtereddfs.append(self.editdfs(df))


    # creates matplotlib pop-up window to analyze one molecule at a time
    def quickplot(self, paired_df):
        plt.figure(figsize=(10,6))
        plt.plot(paired_df['time'], paired_df['acceptor'], label='Acceptor', color='red')
        plt.plot(paired_df['time'], paired_df['donor'], label='Donor', color='green')
        

        plt.xlabel('Time (s)')
        plt.ylabel('Intensity (AU)')
        plt.xlim(1, 100)
        plt.ylim(-100, THRESHOLD)
        plt.title('Donor and Acceptor Intensities Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()


    def parse(self):

        # 1. INPUT FILE PATH HERE SHOULD POINT DIRECTLY AT .TRACES FILE
        path = self.path
        
        # open file and read binary into readable format
        # data put into a one-column DataFrame (fancy table)
        with open(path, "rb") as signals:
            data = signals.read()
            values = np.frombuffer(data, dtype='<i2')
            df = pd.DataFrame(values, columns=['value'])
        
        # Extract metadata from the top of the file
        frames = int(df.iloc[0, 0])              # Frames per molecule
        signals = int(df.iloc[2, 0])              # Total number of signals (donor + acceptor)
        pairs = signals // 2                          # Number of molecules
        print(f"total: {signals}, frames: {frames}, pairs: {pairs}")
        
        # Drop metadata rows
        data = df.iloc[3:].reset_index(drop=True)
        
        # Reshape data into donor and acceptor columns
        data = pd.DataFrame({
        'donor': data['value'][::2].reset_index(drop=True),
        'acceptor': data['value'][1::2].reset_index(drop=True)
        })

        # Add a frame number to each row
        data['frame'] = data.index // pairs * TIME
        # Add a molecule ID to each row
        data['molecule'] = data.index % pairs

        # Group data from each molecule into a DataFrame (fancy table) 
        # and collect DataFrames into a list
        dfs = [
            mol_df.sort_values('frame').reset_index(drop=True)
            for _, mol_df in data.groupby('molecule')
        ]
        
        # remove index from each DataFrame
        for df in dfs:
            df = df.reset_index(drop=True)

        return dfs
    
    def editdfs(self, df):
        # exclude outliers: any value over these thresholds is excluded from the plot
        donor_threshold = THRESHOLD
        acceptor_threshold = THRESHOLD
        df_filtered = df.copy()
        df_filtered['donor'] = df_filtered['donor'].where(df_filtered['donor'] <= donor_threshold, np.nan)
        df_filtered['acceptor'] = df_filtered['acceptor'].where(df_filtered['acceptor'] <= acceptor_threshold, np.nan)
        
        # fill in gaps between excluded points with a straight line
        df_filtered['donor'] = df_filtered['donor'].interpolate(method='linear')
        df_filtered['acceptor'] = df_filtered['acceptor'].interpolate(method='linear')

        # Apply smoothing: this is also done in the Matlab program
        # rolling average helps to prevent some noise
        window_size = WINDOW
        df_filtered['donor_smoothed'] = df_filtered['donor'].rolling(window=window_size, min_periods=1, center=True).mean()
        df_filtered['acceptor_smoothed'] = df_filtered['acceptor'].rolling(window=window_size, min_periods=1, center=True).mean()

        # arrange data to be in the time/donor/acceptor format
        finaldata = pd.DataFrame()
        finaldata["time"] = df_filtered["frame"]
        finaldata["donor"] = df_filtered["donor_smoothed"]
        finaldata["acceptor"] = df_filtered["acceptor_smoothed"]

        return finaldata

    def getData(self):
        # should return a list of dataframes with columns "time", "donor", "acceptor"
        return self.filtereddfs

def main():
    path = "/Users/katejackson/Desktop/Rev1 data/May30_23b/(1) 1&9, 50 mM KCl 5 mM Mg/hel16.traces"
    read = TraceReader(path)
    test = read.getData()[0]
    print(test)
    read.quickplot(test)
    


if __name__ == "__main__":
    main()
    
