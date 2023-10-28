SHELL = /bin/bash


FIREFOX_INPUT = var/inputs/places.sqlite
FIREFOX_OUTPUT = var/outputs/firefox_urls.txt
FIREFOX_SQL_QUERY = "SELECT url FROM moz_places WHERE url LIKE 'https://www.bing.com/images/create/%'"


h help:
	@grep '^[a-z]' Makefile


install:
	pip install pip --upgrade
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

upgrade:
	pip install pip --upgrade
	pip install -r requirements.txt --upgrade
	pip install -r requirements-dev.txt --upgrade


app:
	python -m bing_ai_scraper

# Convert Firefox DB file into URLS text file.
firefox:
	[[ -f $(FIREFOX_INPUT) ]] || { echo 'Cannot find $(FIREFOX_INPUT)'; exit 1 ;}
	sqlite3 $(FIREFOX_INPUT) $(FIREFOX_SQL_QUERY) | cut -f1 -d? | sort | uniq > $(FIREFOX_OUTPUT)
