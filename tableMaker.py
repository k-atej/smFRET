from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure


# makes a single histogram from a given data frame column
#   - data: pandas dataframe to input into a table
#   - master: which frame of the gui to add the table to
#   - row: which row to add canvas to
#   - col: which column to add canvas to
def makeTable(data, master, row, col):
    fig = Figure(dpi=100)
    ax = fig.add_subplot()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    ax.table(cellText=data.values, colLabels=data.columns, loc='center')
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().grid(row=row, column=col)

# adds another column to the dataframe, calculating eFRET from the columns labeled donor and acceptor
#   - data: pandas dataframe containing input data
def efretCalculator(data):
    data["eFRET"] = (data["acceptor"] / (data["donor"] + data["acceptor"]) )
    print(data)
    