# Bing Image Creator Scraper
> Download your AI images and prompts, based on relevant URLs in your browser history

While Bing Image Creator lets you create many images from prompts and these can be access by URL, the history of the web app is limited to a small number of items.

If you entered a prompt and got a result, the results will be in your browser's history. So this project lets you take the AI imag eURLs from your history and then run a Python script to download them all to your machine.


## Bing Image Creator

Go to here

https://www.bing.com/images/create

Sign into Microsoft if needed.

Go to the _Creations_ tab.

Note that your recent history is limited to a fixed number of items, but the others are still there.


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
