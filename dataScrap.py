from bs4 import BeautifulSoup
from collections import defaultdict
from pathlib import Path
import pandas as pd


class webScraping:

    def __init__(self, url, tagName, tagClass):
        self.url = url
        self.tagName = tagName
        self.tagClass = tagClass
        self.content = None
        self.rawTagData = None
        self.cleanTagData = None
        self.panda = None

    def parseData(self):
        file = Path(__file__).with_name(self.url)
        with open(file, "r") as fileOpen:
            fileContents = fileOpen.read()
            self.content = BeautifulSoup(fileContents, 'html.parser')
        # print(self.content)

    def extractTags(self):
        if self.content is not None:
            extractedTags = self.content.find(self.tagName, class_=self.tagClass)
            self.rawTagData = extractedTags
            # print(self.rawTagData)
        else:
            return None

    def cleanTags(self):
        rows = self.rawTagData.find_all('tr')
        cleanDict = defaultdict(dict)
        index = 0

        for row in rows:
            columns = row.find_all(['td'])
            colData = []

            for col in columns:
                data = col.text.strip()
                colData.append(data)

            cleanDict[index] = colData
            index += 1

        self.cleanTagData = cleanDict


    def makePanda(self):
        df = pd.DataFrame.from_dict(self.cleanTagData, orient='index', columns=['Name', 'Distance', 'Orbital Period'])
        df = df.dropna()
        self.panda = df

    def printData(self):
        print(self.cleanTagData)

    def run(self):
        try:
            self.parseData()
            if self.content:
                self.extractTags()
                self.cleanTags()
                self.makePanda()
                self.printData()
        except Exception as e:
            print("An error occurred:", e)




if __name__ == "__main__":
    fileName = 'Dwarfplanets.html'

    scrap = webScraping(fileName, "table", None)
    scrap.run()




