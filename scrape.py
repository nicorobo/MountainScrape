# scrape.py

import sys
import time
import rest
from soup import serve_soup
from area import scrape_area
from route import scrape_route

mainUrl = "https://www.mountainproject.com"

# Setup flags
apiFlag = '--api' in sys.argv
routeFlag = '--route' in sys.argv

def scrape(url, areas, areasID, locations):
	# Acquire hot soup
	soup = serve_soup(mainUrl+url)
	# Retrieve area data and initialize areaID
	areaData = scrape_area(soup, url, areas, areasID, locations)
	areaID = None
	if apiFlag:
		# Get area's id and remove quotes
		areaID = rest.post('/areas', areaData).text[1:-1]

	links = get_area_links(soup)

	if len(links) > 0:
		for link in links:
			# If location is a unique value, add it to locations. Otherwise, just send locations
			currentLocation = areaData["location"]
			nextLocations = locations if areaData["locationInherited"] and currentLocation == None else locations+[currentLocation]
			time.sleep(0.5)
			# Recursively repeat this function with the found areas
			scrape(link.attrs["href"], areas+[link.getText()], areasID+[areaID], nextLocations)
	else:
		links = get_route_links(soup)
		for link in links:
			print(link.getText())
			if routeFlag:
				time.sleep(0.1)
				routeData = scrape_route(link, areas, areasID+[areaID])
				if apiFlag:
					rest.post('/routes', routeData)

def get_area_links(soup):
	return soup.find("div", {"class": "rspCollapsedContent"}).findAll("a", target="_top")

def get_route_links(soup):
	arr = []
	routeTable = soup.find("table", {"id": "leftNavRoutes"})
	if(routeTable != None):
		arr = soup.find("table", {"id": "leftNavRoutes"}).findAll("a");
	return arr

# Begin to process pages. 
# Terminal arguments are the unique area-specific url, and the name of the area
# Example: python3 mountainScrape.py /v/echo-canyon/105868640 "Echo Canyon" 
scrape(sys.argv[len(sys.argv)-2], [sys.argv[len(sys.argv)-1]], [], [])

