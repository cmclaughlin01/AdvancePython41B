from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd
from urllib.request import urlopen
import unittest


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
        content = urlopen(self.url)
        self.content = BeautifulSoup(content, 'html.parser')

    def extractTags(self):
        if self.content is not None:
            extractedTags = self.content.find(self.tagName, class_=self.tagClass)
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

    def makePanda(self):
        thead = self.content.find('thead')
        headers = [th.text.strip() for th in thead.find_all('th')[1:]]
        df = pd.DataFrame(self.cleanTagData, index=headers, columns=None)

        self.panda = df

    def printData(self):
        print(self.panda)

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
    fileName = 'https://gml.noaa.gov/aggi/aggi.html'

    scrap = webScraping(fileName, "table", None)
    scrap.run()

    #unittest.main()





