# route.py

import re
import grades
import printer
from soup import serve_soup

mainUrl = "https://www.mountainproject.com"

# Scrape a route and return its data
def scrape_route(link, areas, areasID):
	name = link.getText()
	url = link.attrs["href"]
	# Acquire hot soup
	soup = serve_soup(mainUrl+url)
	routeData = {
		"name": name,
		"parents": areas,
		"parentsID": areasID,
		"url": mainUrl+url,
		"info": get_info(soup)
	}
	printer.route(routeData["info"])
	return routeData

# Get the details of a particular route
def get_info(soup):
	# Get route type information
	routeType = soup.find("span", itemtype="http://data-vocabulary.org/Review-aggregate") .find("td", text=re.compile("Type.*")) .findNext('td').getText().split(",") 
	grade = scrape_grades(soup)
	routeInfo = {
		"grade": grade,
		"pitches": get_pitches(routeType),
		"commitment": get_commitment(routeType),
		"style": get_style(routeType),
		"height": get_height(routeType),
		"primaryGrade": get_primary_grade(grade)
	}
	return routeInfo

# Get the number of pitches the route has
def get_pitches(routeType):
	for part in routeType:
		part = part.strip()
		if "pitch" in part or "pitches" in part:
			pitches = [int(s) for s in part.split() if s.isdigit()][0]
			return pitches
	return 1

# Get a routes commitment grade
def get_commitment(routeType):
	commitmentGrades = {
		"I": 1,
		"II": 2,
		"III": 3,
		"IV": 4,
		"V": 5,
		"VI": 6,
		"VII": 7,
	}
	for part in routeType:
		part = part.strip()
		if "Grade" in part:
			grade = part.split(' ')[1]
			if grade in commitmentGrades:
				gradeDict = {"string": grade, "value": commitmentGrades[grade]}
				return gradeDict
			else:
				printer.error('parsing commitment', grade)
				return None
	return None

# Get an array of the route's climbing styles
def get_style(routeType):
	styleDict = ["TR", "Aid", "Sport", "Trad", "Boulder", "Ice", "Mixed", "Alpine", "Snow"]
	style = []
	for part in routeType:
		part = part.strip()
		if part in styleDict:
			style+=[part]
	return style

# Get the height of the route
def get_height(routeType):
	for part in routeType:
		part = part.strip()
		if "\'" in part:
			part = part.split('\'')
			if len(part) == 2 and part[1] == '':
				return int(part[0])
	return None

def get_primary_grade(grade):
	for gradeType in ["rock", "mixed", "ice", "aid", "boulder"]:
		if grade[gradeType]:
			return gradeType
	return None

def get_yds(yds):
	string = yds.get_text().split(":")[1].strip()
	if "Easy 5th" in string: 
		string = "easy5th"
	return string.strip()

def get_hueco(hueco):
	return hueco.get_text().split(":")[1].strip()

# Get all of the grades for a climb
def scrape_grades(soup):
	gradeData = []
	yds = soup.h3.find("span", {"class": "rateYDS"})
	hueco = soup.h3.find("span", {"class": "rateHueco"})
	if yds:
		gradeData+=[get_yds(yds)]
	if hueco:
		gradeData+=[get_hueco(hueco)]
	for child in soup.h3.children:
		if child.next_sibling == None and not hasattr(child, 'contents'):
			child = child.strip()
			if child not in ["Mod. Snow", "Easy Snow", "Steep Snow"]:
				child = child.split()
				for str in child:
					gradeData+=[str]
			else: 
				gradeData+=[child]
	return get_grades(gradeData)

def get_grades(data):
	gradeDict = {"rock": None, "aid": None, "ice": None, "mixed": None, "boulder":None, "snow": None, "danger":None}
	for part in data:
		if "5." in part or part in "easy5th 4th 3rd":
			gradeDict["rock"] = get_rock_grade(part)
		elif re.search("(A[0-9]|C[0-9])", part):
			gradeDict["aid"] = get_aid_grade(part)
		elif re.match("V([0-9]|-easy|\?)", part):
			gradeDict["boulder"] = get_boulder_grade(part)
		elif part in "G PG PG13 R X":
			gradeDict["danger"] = get_danger(part)
		elif re.match("WI([0-9]*)", part):
			gradeDict["ice"] = get_ice_grade(part)
		elif re.match("^M([0-9]*\Z)", part):
			gradeDict["mixed"] = get_mixed_grade(part)
		elif part in ["Mod. Snow", "Easy Snow", "Steep Snow"]:
			gradeDict["snow"] = get_snow_grade(part)
		# elif snow
	return gradeDict

def get_rock_grade(grade):
	grade = grade.lower()
	if grade in grades.rock:
		gradeDict = {"string": grade, "value": grades.rock[grade]}
		return gradeDict
	else:
		printer.error('parsing rock grade', grade)
		return None

def get_aid_grade(grade):
	if grade[1:] in grades.aid:
		gradeDict = {"string": grade, "value": grades.aid[grade[1:]]}
		return gradeDict
	else:
		printer.error('parsing aid grade', grade)
		return None

def get_boulder_grade(grade):
	nov = grade[1:].split("-")
	if len(nov)>1 and nov[1] == "easy":
		value = grades.boulder[nov[1]]
	else:
		if nov[0] in grades.boulder:
			value = grades.boulder[nov[0]]
		else:
			printer.error('parsing boulder grade', grade)
			return None
	gradeDict = {"string": grade, "value": value}
	return gradeDict

def get_danger(danger):
	if danger in grades.danger:
		dangerDict = {"string": danger, "value": grades.danger[danger]}
		return dangerDict
	else:
		printer.error('parsing danger', danger)
		return None

def get_ice_grade(grade):
	if grade in grades.ice:
		gradeDict = {"string": grade, "value": grades.ice[grade]}
		return gradeDict
	else:
		printer.error('parsing ice grade', grade)
		return None

def get_mixed_grade(grade):
	if grade in grades.mixed:
		gradeDict = {"string": grade, "value": grades.mixed[grade]}
		return gradeDict
	else:
		printer.error('parsing mixed grade', grade)
		return None

def get_snow_grade(grade):
	if grade in grades.snow:
		gradeDict = {"string": grade, "value": grades.snow[grade]}
		return gradeDict
	else:
		printer.error('parsing snow grade', grade)
		return None



