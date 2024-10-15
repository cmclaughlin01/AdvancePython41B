import webscrapper
import pandas as pd

class agricultureAverage:
    def __init__(self):
        self.data = None
        self.AvgEmissionsPanda = None

    def calcAvgEmissions(self, data):
        self.data = data
        data['Greenhouse gas emissions from agriculture'] = (
            data['Greenhouse gas emissions from agriculture'].astype(float))

        total = {}
        count = {}

        for index, row in data.iterrows():
            entity = row['Entity']
            emission = row['Greenhouse gas emissions from agriculture']
            if entity in total:
                total[entity] += emission
                count[entity] += 1
            else:
                total[entity] = emission
                count[entity] = 1

        avgEmissions = {}

        for entity in total:
            avgEmissions[entity] = total[entity] / count[entity]

        self.AvgEmissionsPanda = pd.DataFrame(list(avgEmissions.items()),
                                              columns=['Entity', 'Average Emissions'])

    def printEmssionsPanda(self):
        print(self.AvgEmissionsPanda)


if __name__ == "__main__":
    fileName = 'GHGEmissions.html'
    dataFrame = webscrapper.webScraping(fileName, "tbody", None)
    dataFrame.run()

    dataFrame.panda = dataFrame.panda.transpose()

    agricultureAvg = agricultureAverage()
    agricultureAvg.calcAvgEmissions(dataFrame.panda)
    agricultureAvg.printEmssionsPanda()

