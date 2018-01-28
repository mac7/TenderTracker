from bs4 import BeautifulSoup
import requests

#tender platform url, keyword is set manualy for now
url = "https://smarttender.biz/publichni-zakupivli-prozorro/search="
headers = {'User-Agent':'Mozilla/5.0'}

def pageFinder(url, headers, key):

	''' Getting web source and finding out how many pages are there '''

	#get raw smarttender page
	webPage = requests.get(url+key, headers=headers)

	#create object to parse web page
	soup = BeautifulSoup(webPage.text, "html.parser")

	#finding page links and count of pages
	numberOfPages = soup.find('div', attrs = {'id' : 'MainContent_MainContent_MainContent_Pager'}).get_text().strip()

	#return count of pages
    return numberOfPages


def check(keys):

	key = 'інтернет'

	pages = pageFinder(url, headers, key)

	print(pages)

	#data = requests.get(url, headers=headers)

	#%s/?nh=1"%(key, nextPage)  /?p=2&nh=0

	#file = open('smarttender', 'w')
	#file.write(data.text)
	#print('file smarttender created')
	#file.close()

	#create soup object
	#soup = BeautifulSoup(data.text, "html.parser")

	#filtering
	#for item in soup.find_all('div', attrs={"class":"items-list"}):
	#	for link in item.find_all('a'):
	#		if (link.get('href') == ''):
	#			continue
	#		else:
	#			print('https://prozorro.gov.ua/%s'%link.get('href'))
