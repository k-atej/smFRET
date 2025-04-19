from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure



# creates a histogram to display in the histogramWindow
class DistributionMaker():
#   - data: pandas dataframe 
#   - datacol: column from data to input to histogram
#   - savepath: what to set as the default save path
#   - master: which frame of the gui to add the histogram to
#   - row: which row to add canvas to
#   - col: which column to add canvas to
#   - upper: upper intensity cutoff
#   - lower: lower intensity cutoff 


    def __init__(self, data, datacol, savepath, master, row, col, upper, lower):
        self.data = data
        self.datacol = datacol
        self.savepath = savepath
        self.master = master
        self.row = row
        self.col = col
        self.upper = upper
        self.lower = lower
        
        if self.upper is not None:
            if self.lower is not None:
                self.upper = float(self.upper)
                self.lower = float(self.lower)
                self.trimdata()
        self.fig = self.makeHistogram()

    def trimdata(self):
        #select for data with intensity between upper and lower limits
        data = self.data.loc[(self.data['intensity'] >= self.lower) & (self.data['intensity'] <= self.upper)]
        self.data = data


    # makes a single histogram from a given data frame column
    def makeHistogram(self):

        # create a new matplotlib figure
        fig = Figure(dpi=75)
        f = fig.gca() #gca = get current axes

        # create a new histogram, set parameters
        f.hist(self.data[self.datacol])

        #set axes
        if self.datacol == "efret":
            f.set_xlim([0, 1])

        #set title & append figure to canvas
        f.set_title(self.datacol)
        fig.tight_layout()
        self.hist_canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.hist_canvas.draw()
        self.hist_canvas.get_tk_widget().grid(row=self.row, column=self.col)

        return fig
    
    def save(self, path):
        filepath = path + "/" + "FRETresult.dat"
        col_widths = [20, 20]
        self.write_fwf(self.data, filepath, col_widths)


        filepath2 = path + "/" + "csvtest.csv"
        self.data.to_csv(filepath2, index=False, header=False)
        
    
    def destroy(self):
        self.hist_canvas.get_tk_widget().destroy()


    def write_fwf(self, df, filepath, col_widths, justify='left'):
        with open(filepath, 'w') as f:
            for _, row in df.iterrows():
                formatted_row = ''
                for i, value in enumerate(row):
                    format_string = '{:<' + str(col_widths[i]) + '}' if justify == 'left' else '{:>' + str(col_widths[i]) + '}'
                    formatted_row += format_string.format(str(value))
                f.write(formatted_row + '\n')
    
    