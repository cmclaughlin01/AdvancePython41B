import json
from collections import defaultdict
from pathlib import Path
import pandas as pd


class webScraping:

    def __init__(self, fileName):
        self.fileName = fileName
        self.content = None
        self.cleanTagData = defaultdict(list)
        self.panda = None

    def parseData(self):
        file = Path(__file__).with_name(self.fileName)
        with open(file, "r") as csvOpen:
            fileContents = csvOpen.readlines()
            self.content = fileContents

    def extractTags(self):
        if self.content is not None:
            headers = self.content[0].strip().split(',')
            for line in self.content[1:]:
                row = line.strip().split(',')
                for i, header in enumerate(headers):
                    if i < len(row):
                        self.cleanTagData[header].append(row[i])
                    else:
                        self.cleanTagData[header].append('')
        else:
            return None

    def makePanda(self):
        self.panda = pd.DataFrame(self.cleanTagData)

    def makeJsonString(self):
        jsonCSV = self.panda.to_json()
        print(jsonCSV)

    def run(self):
        try:
            self.parseData()
            if self.content:
                self.extractTags()
                self.makePanda()
                self.makeJsonString()
        except Exception as e:
            print("An error occurred:", e)



if __name__ == "__main__":
    fileName = 'Dwarfs.csv'

    scrap = webScraping(fileName)
    scrap.run()
