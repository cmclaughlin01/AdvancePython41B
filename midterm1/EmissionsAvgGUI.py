import agricultureAverage
import TkinterGUI
import webscrapper

if __name__ == "__main__":
    fileName = 'GHGEmissions.html'
    dataFrame = webscrapper.webScraping(fileName, "tbody", None)
    dataFrame.run()

    dataFrame.panda = dataFrame.panda.transpose()

    agricultureAvg = agricultureAverage.agricultureAverage()
    agricultureAvg.calcAvgEmissions(dataFrame.panda)
    agricultureAvg.printEmssionsPanda()

    gui = TkinterGUI.dataFramesGui("Average Greenhouse gas emissions from agriculture",
                                   agricultureAvg.AvgEmissionsPanda)
    gui.run()
