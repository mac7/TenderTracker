from bs4 import BeautifulSoup
import requests
import DBWriter

    
#tender platform url, keyword is set manualy for now
url = "https://smarttender.biz/publichni-zakupivli-prozorro/search="
headers = {'User-Agent':'Mozilla/5.0'}

#List of tenderDict
tenderList = []


def pageFinder(url, headers, key):

    ''' Getting web source and finding out how many pages are there '''

    #get raw smarttender page
    webPage = requests.get(url+key, headers=headers)

    #create object to parse web page
    soup = BeautifulSoup(webPage.text, "html.parser")

    #finding page links and count of pages
    return soup.find('div', attrs = {'id' : 'MainContent_MainContent_MainContent_Pager'}).get_text().strip()

def getOwnerID(url, headers):

    ''' Getting owner ID '''

    ownerPage = requests.get(url, headers=headers)
    soup = BeautifulSoup(ownerPage.text, "html.parser")  
    detailedOwnerPage = requests.get('https://Smarttender.biz' + soup.find('iframe')['src'], headers=headers)
    soup2 = BeautifulSoup(detailedOwnerPage.text, "html.parser")
    return int(soup2.find('span', class_ = "info_usreou").get_text())



def main():
    
    #setup keyword
    key = 'інтернет'

    #count of pages in search result
    pages = pageFinder(url, headers, key)

    for page in pages:

        #create link with current page number
        webPage = requests.get(url+key+f'?p={page}', headers=headers)

        #soup objct to parse web page
        soup = BeautifulSoup(webPage.text, 'html.parser')

        #find tender data div (with all needed data)
        tenders = soup.find('div', class_ = 'tenders')

        for headOfTable in tenders.find_all('tr', class_ = "head"):

            #tender deadline
            try:
                timeStartEnd = []
                deadlines = headOfTable.find('td', class_ ="col6")
                for deadline in deadlines.find_all('div'):
                    timeStartEnd.append(deadline.get_text().strip())

            except:
                timeStartEnd = ['No data', 'No data']

            if (len(timeStartEnd) == 0):
                timeStartEnd = ['No data', 'No data']

            #tender number
            tenderNumber = headOfTable.find('td', class_ = 'col1').get_text().strip()

            #tender details
            tenderPageLink = headOfTable.find('a', class_ = 'linkSubjTrading')['href']

            #tender name
            tenderName = headOfTable.find('a', class_ = 'linkSubjTrading').get_text().strip()

            #tender price
            tenderPrice = headOfTable.find('span', class_ = "InitRate").get_text().strip()

            #tender host
            tenderOwner = headOfTable.find('a', class_ ="organizer-popover").get_text().strip()

            #tender owner details
            #tenderOwnerAcc = headOfTable.find('div', class_ = "hidden").get_text().strip() + ' https://smarttender.biz' + headOfTable.find('a', class_ = "organizer-popover", target="_blank")['href']

            #tender uploaded
            tenderStart = timeStartEnd[0]

            #submit till
            tenderEnd = timeStartEnd[1]

            #Dict with tender information
            tender = {
                'tenderNumber': tenderNumber,
                'tenderPageLink': tenderPageLink,
                'tenderName' : tenderName,
                'tenderPrice' : tenderPrice,
                'tenderOwner' : tenderOwner,
                'tenderOwnerID' : getOwnerID(tenderPageLink, headers),
                'tenderStart' : tenderStart,
                'tenderEnd' : tenderEnd
            }

            tenderList.append(tender)
            
    DBWriter.DBInsert(tenderList[0])


if __name__ == "__main__":
    main()
