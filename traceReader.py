import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# THREE WAYS TO USE THIS SCRIPT:
# 1. CHANGE THE FILE PATH IN "NEWMAIN" FUNCTION AND RUN THIS FILE TO SEE A TRACE
# 2. CHANGE THE MOLECULE NUMBER IN "NEWMAIN" FUNCTION TO SEE DIFFERENT TRACES
# 3. CHANGE THE DF VARIABLE IN "NEWMAIN" FUNCTION TO SEE THE FILTERED DATA

TIME = 0.1 # time resolution

# creates matplotlib pop-up window to analyze one molecule at a time
def quickplot(paired_df):
    plt.figure(figsize=(10,6))
    plt.plot(paired_df['frame'], paired_df['acceptor'], label='Acceptor', color='red')
    plt.plot(paired_df['frame'], paired_df['donor'], label='Donor', color='green')
    

    plt.xlabel('Frame')
    plt.ylabel('Intensity')
    plt.xlim(1, 100)
    plt.ylim(-100, 1000)
    plt.title('Donor and Acceptor Intensities Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()


def newmain():

    # 1. INPUT FILE PATH HERE SHOULD POINT DIRECTLY AT .TRACES FILE
    path = "/Users/katejackson/Desktop/Rev1 data/May30_23b/(1) 1&9, 50 mM KCl 5 mM Mg/hel16.traces"
    
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

    # for our brief analysis, we will just look at one DataFrame in the list:
    # in this case, we are looking at the first DataFrame
    # containing the data from the first molecule
    # 2. INCREMENT THE NUMBER BELOW TO SEE DIFFERENT MOLECULES
    df = dfs[0]
    
    # Apply smoothing: this is also done in the Matlab program
    # rolling average helps to prevent some noise
    window_size = 3
    df['donor_smoothed'] = df['donor'].rolling(window=window_size, center=True).mean()
    df['acceptor_smoothed'] = df['acceptor'].rolling(window=window_size, center=True).mean()

    # exclude outliers: any value over these thresholds is excluded from the plot
    donor_threshold = 5000
    acceptor_threshold = 5000
    df_filtered = df.copy()
    df_filtered['donor'] = df_filtered['donor'].where(df_filtered['donor'] <= donor_threshold, np.nan)
    df_filtered['acceptor'] = df_filtered['acceptor'].where(df_filtered['acceptor'] <= acceptor_threshold, np.nan)
    
    # fill in gaps between excluded points with a straight line
    df_filtered['donor'] = df_filtered['donor'].interpolate(method='linear')
    df_filtered['acceptor'] = df_filtered['acceptor'].interpolate(method='linear')

    # display the data
    # 3. CHANGE "DF" TO "DF_FILTERED" TO SEE DATA AFTER OUTLIERS HAVE BEEN EXCLUDED
    print(df)
    quickplot(df)


newmain()
    
