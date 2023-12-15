SHELL = /bin/bash
APP_DIR = imagescraper

FIREFOX_INPUT = var/inputs/places.sqlite
FIREFOX_OUTPUT = var/outputs/firefox_urls.txt
FIREFOX_SQL_QUERY = "SELECT url FROM moz_places WHERE url LIKE 'https://www.bing.com/images/create/%'"
DEBUG_TEST_URL = https://www.bing.com/images/create/a-beautiful-purple-and-yellow-flower-with-water-dr/651328ae9a6646c9b1b66c9a26c1bf2f

export PYTHONPATH


default: install install-dev

all:  install install-dev fmt-check lint typecheck


h help:
	@grep '^[a-z]' Makefile


.PHONY: hooks
hooks:
	cd .git/hooks && ln -s -f ../../hooks/pre-push pre-push


install:
	pip install pip --upgrade
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

upgrade:
	pip install pip --upgrade
	pip install -r requirements.txt --upgrade
	pip install -r requirements-dev.txt --upgrade


fmt:
	black .
	isort .

fmt-check:
	black . --diff --check
	isort . --diff --check-only

pylint:
	source .env \
		&& pylint $(APP_DIR) \
		|| pylint-exit $$?

flake8:
	# Error on syntax errors or undefined names.
	flake8 . --select=E9,F63,F7,F82 --show-source
	# Warn on everything else.
	flake8 . --exit-zero

lint: pylint flake8

fix: fmt lint


t typecheck:
	mypy $(APP_DIR)


# Convert Firefox DB file into URLS text file.
firefox:
	[[ -f $(FIREFOX_INPUT) ]] || { echo 'Cannot find $(FIREFOX_INPUT)'; exit 1 ;}

	sqlite3 $(FIREFOX_INPUT) $(FIREFOX_SQL_QUERY) \
		| cut -f1 -d? | sort | uniq > $(FIREFOX_OUTPUT)
	echo "File created at: $(FIREFOX_OUTPUT)"

# Extract prompts and images from text file of URLs.
app:
	python -m imagescraper

debug:
	python -m imagescraper $(DEBUG_TEST_URL)
