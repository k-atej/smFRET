import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as mplt
import os

def main():
    data =  {'A': [1, 2, 3, 4, 3, 3, 4, 2, 1, 3], 'B': [2, 4, 6, 8, 4, 4, 4, 4, 4, 4], 'C': [3, 6, 9, 12, 3, 3, 3, 3, 3, 3]}
    df = pd.DataFrame(data=data)
    app = Application(df)
    app.mainloop()

class Application(tk.Tk):

    def __init__(self, df):
        super().__init__()
        self.title("Testing Again")
        self.df = df

        self.frame = ttk.Frame(self)
        self.frame.grid(row=0, column=1)

        #self.text_list = tk.Listbox(self.frame)
        #self.text_list.grid(row=1, column=0)
        #self.text_list.insert(tk.END, df)

        self.table()
        self.his()

    def table(self): # i may want to turn this into a class
        
        #sets default matplotlib color params
        plt.rcParams["axes.prop_cycle"] = plt.cycler(
            color=["#4C2A85", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC"]
        )

        #create a figure table from the sample data
        fig = Figure(figsize=(2, 2), dpi=100)
        ax = fig.add_subplot()
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')
        ax.table(cellText=self.df.values, colLabels=self.df.columns, loc='center')
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)

        #toolbar = NavigationToolbar2Tk(canvas, self)
        #toolbar.update()
        #canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    
    def his(self): #creates histogram from sample data
        fig = Figure(figsize=(2.5, 2.5), dpi=100)
        f = fig.gca() #gca = get current axes
        f.hist(self.df["A"], bins=4)
        f.set_xlabel("x label")
        f.set_ylabel("y label")
        f.set_title("sample histogram: 'A'")
        fig.tight_layout()
        hist_canvas = FigureCanvasTkAgg(fig, master=self.frame)
        hist_canvas.draw()
        hist_canvas.get_tk_widget().grid(row=0, column=1)

main()