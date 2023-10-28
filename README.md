# Bing Image Creator Scraper
> Bulk-download your AI images and prompts created with Bing, based on relevant URLs you provide from your browser history


## Why

While Bing Image Creator lets you create many images from prompts and these can be access by URL, the history of the web app is limited to a small number of items so you cannot navigate to your old creations unless you know the exact URL. So this means most of your creations could be lost.

If you entered a prompt and got a result, then that page of creations will actually exist in your browser's history (at least until you clear it, so it could be a very long time). This

This project takes advantage of this - it lets you take the AI image URLs from your history, as far back as possible, and then run a Python script to download them all to your machine.

And then you can analyze to see what text works best based on your image results, and then you can go and back even better images.


## Bing Image Creator

How to use the tool:

1. Go here: https://www.bing.com/images/create
1. Sign into Microsoft if needed.
1. Enter a prompt and click _Create_.
1. Go to the _Creations_ tab.


## Browser history

You should go through each browser on each computer where you use Bing Image Creator to create images. If you put those together as one list of URLs, then you should cover everything you made (as long as you didn't clear your history).


### Firefox

Go to this directory in Windows.

```
C:\Users\<username>\AppData\Roaming\Mozilla\Firefox\Profiles
```

Find your relevant profile directory.

Find `places.sqlite`.

Copy it into this repo to the `var/inputs` directory.

Get relevant URLS out:

```sh
sudo apt install sqlite3
```

Run

The last bit strips out everything from query parameters (`?`) onwards and removes duplicates.

### Edge

1. Go to History (CTRL+H).
1. click the menu (three dots).
1. Click _Export browsing history_.
1. Click to confirm, pick a location.
