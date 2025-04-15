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


    def __init__(self, data, datacol, savepath, master, row, col):
        self.data = data
        self.datacol = datacol
        self.savepath = savepath
        self.master = master
        self.row = row
        self.col = col
        

        self.fig = self.makeHistogram()


    # makes a single histogram from a given data frame column
    def makeHistogram(self):

        # create a new matplotlib figure
        fig = Figure(dpi=50)
        f = fig.gca() #gca = get current axes

        # create a new histogram, set parameters
        f.hist(self.data[self.datacol])


        #set title & append figure to canvas
        f.set_title(self.datacol)
        fig.tight_layout()
        self.hist_canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.hist_canvas.draw()
        self.hist_canvas.get_tk_widget().grid(row=self.row, column=self.col)

        return fig
    
    def destroy(self):
        self.hist_canvas.get_tk_widget().destroy()

    
    