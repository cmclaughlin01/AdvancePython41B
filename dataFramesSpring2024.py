from bs4 import BeautifulSoup
from collections import defaultdict
from pathlib import Path
import pandas as pd
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
        file = Path(__file__).with_name(self.url)
        with open(file, "r") as fileOpen:
            fileContents = fileOpen.read()
            self.content = BeautifulSoup(fileContents, 'html.parser')

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


class testWebScraping(unittest.TestCase):
    def setUp(self):
        self.fileName = 'GHGEmissions.html'
        self.testScrap = webScraping(self.fileName, "tbody", None)
        self.testScrap.run()

    def testStructure(self):
        df = self.testScrap.panda
        self.assertIn('Entity', df.index)
        self.assertIn('Greenhouse gas emissions from waste', df.index)
        self.assertTrue(isinstance(df, pd.DataFrame))


if __name__ == "__main__":
    fileName = 'GHGEmissions.html'

    scrap = webScraping(fileName, "tbody", None)
    scrap.run()

    #unittest.main()





