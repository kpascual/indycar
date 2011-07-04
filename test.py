import urllib2
from BeautifulSoup import BeautifulSoup
import csv
import time
import datetime


def writeToCsv(filename, data):
    writer = csv.writer(open(filename,'ab'),lineterminator='\n',delimiter='\t')
    writer.writerows(data)


def getHtml(url):
    response = urllib2.urlopen(url)
    doc = response.read()

    return doc


def getLeaderboard(html):
    soup = BeautifulSoup(html)

    results = soup.findAll(attrs={'id':'TimingScoringTable'})

    final_data = [] 
    for itm in results:
        rows = itm.findAll('tr')
        for row in rows:
            cells = row.findAll('td')
            rowdata = [cell.renderContents() for cell in cells]

            try:            
                if int(rowdata[0]) in range(1,34):
                    final_data.append(rowdata)
            except:
                pass

    return final_data


def getLapNumber(html):
    soup = BeautifulSoup(html)

    lap_count = soup.find('span',attrs={'id': 'LapNumberLabel'})
    total_laps = soup.find('span',attrs={'id': 'TotalLapsLabel'})

   
    return (lap_count.renderContents(), total_laps.renderContents()) 


def main():
    url = 'http://racecontrol.indycar.com'
    html = getHtml(url) 
    data = getLeaderboard(html)
    lap_data = getLapNumber(html)

    appended_data = []
    for row in data:
        row.extend(lap_data)
        row.append(datetime.date.now())
        appended_data.append(row)

    writeToCsv('texas.csv',appended_data)




def findCurrent():
    url = 'http://racecontrol.indycar.com'
    html = getHtml(url) 
    print html 


if __name__ == '__main__':
    #main()
    findCurrent()
