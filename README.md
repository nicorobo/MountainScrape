# MountainScrape
🌄 A python script for scraping Mountain Project (for educational purposes)

## Using MountainScrape

<img src="https://dl.dropboxusercontent.com/s/h7mbwxnupfqnzid/Screenshot%202017-03-08%2018.50.27.png" alt="MountainScrape Demo" width="600px"/>

### Dependencies

While in the root directory, install dependencies with `pip3 install -r requirements.txt`.

### Running Scraper

Enter `python3 scrape.py` followed by the root area's URL identifier, starting with /v/ (ex: */v/echo-canyon/105868640*) and the root areas name as a string (ex: *"Echo Canyon"*). This is temporary, soon you won't have to explicitly enter the name.

Scraping just the areas *(but not sending it anywhere)* would look like this: `python3 scrape.py /v/echo-canyon/105868640 "Echo Canyon"`

If you'd like to scrape the routes, include the --route flag. `python3 scrape.py --route /v/red-rock/105731932 "Red Rock"`

If you want the scraper to make formatted HTTP **PUT** requests, set up your API endpoint in `scraper.py`, and include the --db flag. `python3 scrape.py --route --db /v/lovers-leap/105733959 "Lover's Leap"`
