import matplotlib.pyplot as plt
import pandas as pd

class PlotManager:
    def __init__(self, df: pd.DataFrame):
        self.df = df
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


class createDataPanda:
    def __init__(self, filepath):
        self.filepath = filepath
        self.panda = None

    def parseData(self):
        self.panda = pd.read_csv(self.filepath)

    def printPanda(self):
        print(self.panda)

    def runPanda(self):
        self.parseData()
        # self.printPanda()



if __name__ == "__main__":
    fileName = 'Dwarfs.csv'

    scrap = createDataPanda(fileName)
    scrap.runPanda()

    dataPanda = scrap.panda

    plot_manager = PlotManager(dataPanda)

    plot_manager.plot_line('Dwarf', 'Distance(AU)', title='Dward Distance(AU)')
    plot_manager.plot_bar('Dwarf', 'Distance(AU)', title='Dward Distance(AU)')
    plot_manager.plot_scatter('Dwarf', 'Period(years)', title='Dwarf Period(years)')

