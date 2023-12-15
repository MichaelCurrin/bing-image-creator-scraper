# Usage

Using this project's `Makefile`, you can extract relevant URLs from a Firefox database and then use Python to process all of them.


## View available make commands

```sh
$ make help
```


## Browser history

Follow the steps in [Browser history](browser-history.md) to prepare your data.


## Run

Run application to scrape all data for text file of URLs. If you have Firefox and Edge URLs, all will be used.

```sh
$ make app
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
