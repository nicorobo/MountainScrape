# soup.py

import requests
from bs4 import BeautifulSoup

# Prepare scraper client
session = requests.Session()
headers = {
	"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36", 
	"Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"
	} 

def serve_soup(url):
	# Retrieve page at url using our session
	html = session.get(url=url, headers=headers)
	soup = BeautifulSoup(html.text, "html.parser")
	return soup