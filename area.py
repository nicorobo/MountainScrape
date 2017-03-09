# area.py

import printer

mainUrl = "https://www.mountainproject.com"

def scrape_area(soup, url, areas, areasID, locations):
	parent = None if len(areas) < 2 else areas[-2]
	parentID = None if len(areasID) < 1 else areasID[-1]
	location = get_location(soup, locations)
	printer.area(areas[-1], location[0])
	areaData = {
		"name": areas[-1],
		"parents": areas[:-1], 
		"parentsID": areasID,
		"location": location[0],
		"locationInherited": location[1],
		"url": mainUrl+url
	}
	return areaData

def get_location(soup, locations):
	table = soup.find('div', id="rspCol800").find("div", {"class": "rspCol"}).table
	for tr in table.findAll('tr'):
		if tr.td.string is not None and "Location" in tr.td.string:
			location = tr.td.next_sibling.find(text=True)
			location = location.split(", ")
			lat = location[0]
			lng = location[1].split('\xa0')[0]
			location = [lng, lat]
			return [location, False]
	# Location has not been set, check parents
	if len(locations) > 0:
		return [locations[-1], True]
	else:
		return [None, False]