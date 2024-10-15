import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import linregress

class PlotManager:
    def __init__(self, df: pd.DataFrame, data):
        self.df = df
        self.data = data
        plt.figure(figsize=(10, 6)) 

    def plot_line(self, xColumn, yColumn, title=None, xLabel=None, yLabel=None):
        plt.plot(self.df[xColumn], self.df[yColumn], marker='o')
        plt.title(title if title else f'Line Plot of {yColumn} vs {xColumn}')
        plt.xLabel(xLabel if xLabel else xColumn)
        plt.yLabel(yLabel if yLabel else yColumn)
        plt.grid(True)
        plt.show()

    def plot_bar(self, xColumn, yColumn, title=None, xLabel=None, yLabel=None):
        plt.bar(self.df[xColumn], self.df[yColumn])
        plt.title(title if title else f'Bar Plot of {yColumn} vs {xColumn}')
        plt.xLabel(xLabel if xLabel else xColumn)
        plt.yLabel(yLabel if yLabel else yColumn)
        plt.grid(True)
        plt.show()

    def plot_scatter(self, xColumn, yColumn, title=None, xLabel=None, yLabel=None):
        plt.scatter(self.df[xColumn], self.df[yColumn], marker='o')
        plt.title(title if title else f'Scatter Plot of {yColumn} vs {xColumn}')
        plt.xLabel(xLabel if xLabel else xColumn)
        plt.yLabel(yLabel if yLabel else yColumn)
        plt.grid(True)
        plt.show()

    def plotGas(self, gas):
        rowids = list(self.data[gas].keys())
        concentrations = [float(self.data[gas][rowid]) for rowid in rowids]

        slope, intercept, r_value, p_value, std_err = linregress(rowids, concentrations)

        plt.figure(figsize=(10, 5))
        plt.scatter(rowids, concentrations, label=f'Observed {gas} data')
        plt.plot(rowids, intercept + slope * np.array(rowids), 'r', label=f'Fitted line (slope={slope:.4f})')
        plt.xlabel('Year')
        plt.ylabel(f'{gas} Concentration')
        plt.title(f'{gas} Concentration over Time')
        plt.legend()
        plt.show()

    def plotAllGases(self):
        for gas in self.data:
            self.plotGas(gas)
