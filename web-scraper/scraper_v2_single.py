from bs4 import BeautifulSoup
import requests
from csv import writer

from cities import citiesWithEntry

### Counter for result counting
count = 0

### CSV temp header file
headerCSV = ["cityName", "eventName", "dates", "imageUrl"]
### Specify user agent header
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"}

### Base search url
baseUrl = "https://www.ticketone.it/city/" ### NB: city-code
endUrl  = "/concerti-55/?shownoonbookable=true&page=" ### NB: pageNumber
# &page=1 works, so use the extended version in every case
### shownoonbookable=true allows to show even non-bookable events (ie tickets
### sold out). Given the nature of the application, this should be the correct
### choice.

### Create .csv file
fileName = "csv/concerti.csv"
### Iterate through the pages and save results to file
with open(fileName, 'w', encoding="utf-8", newline='') as file:
	### Create the file writer
	fileWriter = writer(file)
	### Write the file header
	fileWriter.writerow(headerCSV)

	### Iterate through the city list
	for cityElement in citiesWithEntry:
		### Counter for search pages
		pageCount = 1
		### Create url for the first link to the city (page=1)
		url = baseUrl + cityElement[0] + "-" + cityElement[1] + endUrl + str(count)
		### Fetch the page content and create BS4 parser
		page = requests.get(url, headers=headers)
		page.raise_for_status()
		soup = BeautifulSoup(page.content, "html.parser")

		### FIRST THING: search if the pagination block exists
		paginationBlock = soup.find("nav", class_="pagination-block")
		### If paginationBlock is None, no other pages are present
		### Set pageCount accordingly to iterate through it
		if paginationBlock is not None:
			### Fetch the page elements from the pagination block
			pages = paginationBlock.find_all("pagination-item", class_="pagination-item")
			### NB: Anche i button per cambiare pagina sono pagination-item con la
			### stessa classe, in teoria non causa problemi per il recupero dei tag
			### dato che in quell'elemento i figli desiderati non esistono.
			### Unica cosa potrebbe sfanculare un po' il conteggio ma amen
			
			### Set pageCount
			pageCount = len(pages)
		
		### Loop pageCount times
		for pageIndex in range (1, pageCount + 1):
			### Fetch the url of the desired page index
			url = baseUrl + cityElement[0] + "-" + cityElement[1] + endUrl + str(pageIndex)
			
			### Request page and create BS4 parser
			page = requests.get(url, headers=headers)
			page.raise_for_status()
			soup = BeautifulSoup(page.content, "html.parser")

			### Search for each result parent div
			searchList = soup.find_all("div", class_="listing-item")
			
			### Iterate through each searchList element to get the events data
			for item in searchList:
				count += 1
				eventName = item.find("div", class_="event-listing-city").text
				dates = item.find("span", class_="listing-data").text
				imageUrl = item.find("img", class_="listing-image").get("data-src") # Get the data-src attribute

				### Write row to the file
				fileWriter.writerow([cityElement[0], eventName, dates, imageUrl])
		print(cityElement[0] + ": found " + str(count))
		count = 0
print("- - - END - - -")
