import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict

class webScraping:

    def __init__(self, url, tagName, tagClass):
        self.url = url
        self.tagName = tagName
        self.tagClass = tagClass
        self.soup = None
        self.rawTagData = None
        self.cleanTagData = None

    def parseData(self):
        content = urlopen(self.url)
        self.soup = BeautifulSoup(content, 'html.parser')

    def extractTags(self):
        if self.soup is not None:
            extractedTags = self.soup.find_all(self.tagName, class_=self.tagClass)
            self.rawTagData = extractedTags
        else:
            return None

    def cleanTags(self):
        if self.rawTagData is not None:
            dataRows = self.rawTagData[0].findAll('tr')[2:]

            emissionsDict = defaultdict(dict)

            for row in dataRows:
                columns = row.findAll('td')

                countryName = columns[0].text.strip()
                data1970 = columns[1].text.strip()
                data1990 = columns[2].text.strip()
                data2005 = columns[3].text.strip()
                data2017 = columns[4].text.strip()
                data2022 = columns[5].text.strip()
                dataTotalPercent = columns[6].text.strip()
                dataPercentChange = columns[7].text.strip()

                emissionsDict[countryName]['1970'] = data1970
                emissionsDict[countryName]['1990'] = data1990
                emissionsDict[countryName]['2005'] = data2005
                emissionsDict[countryName]['2017'] = data2017
                emissionsDict[countryName]['2022'] = data2022
                emissionsDict[countryName]['percent'] = dataTotalPercent
                emissionsDict[countryName]['change'] = dataPercentChange

            self.cleanTagData = emissionsDict

    def errorHandling(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                return True
            else:
                print("404 error: webpage was not found")
                return False
        except:
            print(response.raise_for_status())
            return False

    def scrap(self):
        if self.errorHandling() is True:
            self.parseData()

    def printData(self):
        for country, values in self.cleanTagData.items():
            print(f"{country:35s} 1970: {values['1970']:6s}  1990: {values['1990']:6s}   2005: {values['2005']:6s} "
                  f"2017: {values['2017']:6s} 2022: {values['2022']:6s} Percent Total Change: {values['percent']:5s} "
                  f"Change: {values['change']:5s}")


if __name__ == "__main__":
    urlLink = 'https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capita'

    scrap = webScraping(urlLink, "table", "wikitable")

    scrap.scrap()
    scrap.extractTags()
    scrap.cleanTags()
    scrap.printData()





