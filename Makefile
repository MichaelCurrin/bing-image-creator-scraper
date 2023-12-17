SHELL = /bin/bash
APP_DIR = imagescraper

VAR_DIR = $(APP_DIR)/var
IMG_OUTPUT_PATH = $(VAR_DIR)/creations

CHROME_INPUT_PATH = $(VAR_DIR)/history_raw/chrome.db
FIREFOX_INPUT_PATH = $(VAR_DIR)/history_raw/firefox.db
EDGE_INPUT_PATH = $(VAR_DIR)/history_raw/edge.csv

CHROME_OUTPUT_PATH = $(VAR_DIR)/history_processed/chrome_urls.txt
FIREFOX_OUTPUT_PATH = $(VAR_DIR)/history_processed/firefox_urls.txt
EDGE_OUTPUT_PATH = $(VAR_DIR)/history_processed/edge_urls.txt

BING_CREATE_URL = https://www.bing.com/images/create/
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


# Convert raw history to filtered text files of just Bing creator URLs.
chrome:
	[[ -f $(CHROME_INPUT_PATH) ]] || { echo 'Cannot find $(CHROME_INPUT_PATH)'; exit 1 ;}

	sqlite3 $(CHROME_INPUT_PATH) \
		"SELECT url FROM moz_places WHERE url LIKE '$(BING_CREATE_URL)%'" \
			| cut -f1 -d? > $(CHROME_OUT_PATH)

	@echo "File created at: $(CHROME_OUT_PATH)"
	@echo "With line count:"
	@wc -l < "$(CHROME_OUT_PATH)"

firefox:
	[[ -f $(FIREFOX_INPUT_PATH) ]] || { echo 'Cannot find $(FIREFOX_INPUT_PATH)'; exit 1 ;}

	sqlite3 $(FIREFOX_INPUT_PATH) \
		"SELECT url FROM moz_places WHERE url LIKE '$(BING_CREATE_URL)%'" \
			| cut -f1 -d? > $(FIREFOX_OUTPUT_PATH)

	@echo "File created at: $(FIREFOX_OUTPUT_PATH)"
	@echo "With line count:"
	@wc -l < "$(FIREFOX_OUTPUT_PATH)"

edge:
	[[ -f $(EDGE_INPUT_PATH) ]] || { echo 'Cannot find $(EDGE_INPUT_PATH)'; exit 1 ;}

	grep '$(BING_CREATE_URL)' $(EDGE_INPUT_PATH) | cut -d ',' -f 2 > $(EDGE_OUTPUT_PATH)

	@echo "File created at: $(EDGE_OUTPUT_PATH)"
	@echo "With line count:"
	@wc -l < "$(EDGE_OUTPUT_PATH)"


# Extract prompts and images from text file of URLs.
run:
	python -m imagescraper

debug:
	python -m imagescraper $(DEBUG_TEST_URL)

# How many creation folders exist.
count:
	find $(IMG_OUTPUT_PATH)/* -maxdepth 1 -type d | wc -l

# Reset - delete all creations.
delete:
	rm -rf $(IMG_OUTPUT_PATH)/*
