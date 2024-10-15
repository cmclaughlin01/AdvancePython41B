from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict


def openWebsite(urlTag):
    html = urlopen(urlTag)
    return BeautifulSoup(html, 'html.parser')


def scrapeData(alink):
    soup = openWebsite(alink)

    table = soup.find('table', {'class': 'wikitable'})
    dataRows = table.findAll('tr')[2:]

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

    return emissionsDict


def dataPrint(dataDictionary):
    for country, values in dataDictionary.items():
        print(f"{country:30s} 1970: {values['1970']:4s}  1990: {values['1990']:4s}   2005: {values['2005']:4s} "
              f"2017: {values['2017']:4s} 2022: {values['2022']:4s} Percent Total Change: {values['percent']:4s} "
              f"Change: {values['change']:4s}")


def main():
    urlLink = 'https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capita'

    result = scrapeData(urlLink)

    dataPrint(result)


main()