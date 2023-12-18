# Installation

Clone the repo then continue below.

## Project requirements

- [Python](https://www.python.org/) >= 3.10


## Install system dependencies

### Ubuntu/Debian

Install packages with `apt` if you have it, otherwise `apt-get` can be used instead.

```sh
$ sudo apt update
$ sudo apt install python3
```

Install SQLite3 - this is only needed if you use Firefox and want to process the history in the Firefox's SQLite database.

```sh
sudo apt install sqlite3
```


## Install project dependencies

Create and activate a virtual environment.

```sh
$ python3 -m venv venv
```

```sh
$ source venv/bin/activate
```

### Core dependencies

```sh
$ make install
```

### Dev dependencies

```sh
$ make install-dev
```

You may continue to the [Usage](usage.md) doc.
