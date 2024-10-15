from bs4 import BeautifulSoup
from urllib.request import urlopen
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
        fileContents = urlopen(self.url)
        self.content = BeautifulSoup(fileContents, 'html.parser')

    def extractTags(self):
        if self.content is not None:
            allTags = self.content.find_all(self.tagName, class_=self.tagClass)
            extractedTags = allTags[1] if len(allTags) > 1 else None
            self.rawTagData = extractedTags
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
        # print(self.cleanTagData)

    def makePanda(self):
        allTheads = self.content.find_all('thead')
        thead = allTheads[1] if len(allTheads) > 1 else None
        headers = [th.text.strip() for th in thead.find_all('th')[3:]]
        # print(headers)

        df = pd.DataFrame(self.cleanTagData, index=headers, columns=None)

        self.panda = df.transpose()

    def printData(self):
        print(self.panda)
        
    def cleaveData(self):
        self.panda = self.panda.drop(columns=['Year', 'Total', "1990 = 1", "% change *"])

    def renameData(self):
        self.panda = self.panda.rename(columns={"CFCs*": "CFCs", "HFCs*": "HFCs"})

    def getPanda(self):
        return self.panda

    def run(self):
        try:
            self.parseData()
            if self.content:
                self.extractTags()
                self.cleanTags()
                self.makePanda()
                self.cleaveData()
                self.renameData()
                # self.printData()
        except Exception as e:
            print("An error occurred:", e)
