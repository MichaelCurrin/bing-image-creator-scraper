# Usage

Using this project's `Makefile`, you can extract relevant URLs from a Firefox database and then use Python to process all of them.


## View available make commands

```sh
$ make help
```


## Browser history

Follow the steps in [Browser history](browser-history.md) to make the data available for the scraping application. That will write out text files to the `history_process` directory.


## Run

Run the application to scrape all the URLs across all the text files in the `history_process` directory.

```sh
$ make run
```

Target a specific URL, for example:

```sh
$ make one URL=https://www.bing.com/images/create/a-beautiful-purple-and-yellow-flower-with-water-dr/651328ae9a6646c9b1b66c9a26c1bf2f
```

Count your creations:

```sh
$ make count
```

Delete creations:

```sh
$ make delete
```


## Debug

This is used for testing purposes - to scrape a single hard-coded URL instead of using a text file.

```sh
$ make debug
```
