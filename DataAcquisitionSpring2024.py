from collections import defaultdict
from pathlib import Path
import unittest
import re


class DataAcquisitionSpring:
    def __init__(self, fileName):
        self.fileName = fileName
        self.content = None
        self.tagData = None

    def openHtmlFile(self):
        file = Path(__file__).with_name(self.fileName)
        with open(file, "r") as fileContent:
            self.content = fileContent.read()
        #print(self.content)

    def extractTags(self):
        findTable = r'<table[^>]*>.*?</table>'
        findTags = r'<(th|td)[^>]*>(.*?)</\1>'

        tableMatches = re.findall(findTable, self.content, re.IGNORECASE | re.DOTALL)
        tagMatches = re.findall(findTags, self.content, re.IGNORECASE | re.DOTALL)

        tableMatches = [str(match) for match in tableMatches]
        tagMatches = [f"<{tag[0]}>{tag[1]}</{tag[0]}>" for tag in tagMatches]
        extractedTags = tuple(tableMatches + tagMatches)

        return extractedTags

    def cleanTags(self,tagTuple):
        tagDict = defaultdict(list)

        for tag in tagTuple:
            match = re.match(r'<(\w+)', tag)
            if match:
                tag_name = match.group(1)
                tagDict[tag_name].append(tag)

        return tagDict

    def printTagData(self, tagDict):
        for tag_name, tags in tagDict.items():
            print(f"{tag_name}:")
            for tag in tags:
                print(tag)

if __name__ == "__main__":

    filename = 'Dwarfplanets.html'

    dataAcq = DataAcquisitionSpring(filename)

    dataAcq.openHtmlFile()

    tagTuple = dataAcq.extractTags()

    tagDict = dataAcq.cleanTags(tagTuple)

    dataAcq.printTagData(tagDict)

