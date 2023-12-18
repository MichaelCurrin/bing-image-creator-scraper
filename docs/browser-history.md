# Browser history

Follow steps for one or all browsers. Follow the first section to add the history to the repo and then follow the section at the end to filter the history and convert to text files.


## Export history

### Chrome

1. Open the file explorer.
1. Navigate here:
    ```
    C:\Users\<username>\AppData\Local\Google\Chrome\User Data\
    ```
1. Go into the appropriate user directory. The first user will be called `Default`.
1. Find the `History` file, which is a SQLite database.
1. Copy that file into this repo in the `imagescraper/var/browser_raw` directory named `chome.db`.

### Firefox

1. Open the file explorer.
1. Go to your Firefox profiles directory. Here is the directory in Windows. Note that `AppData` is usually hidden so it's best to enter this path in your file browser.
    ```
    C:\Users\<username>\AppData\Roaming\Mozilla\Firefox\Profiles
    ```
1. Find the relevant directory for your profile and go into it.
1. Find the `places.sqlite` file, which is a SQLite database.
1. Copy that file into this repo in the `imagescraper/var/browser_raw` directory and name it `firefox.db`.

### Edge

1. Open Edge.
1. Go to History (<kbd>CTRL</kbd>+<kbd>H</kbd>).
1. Click the menu (three dots).
1. Click _Export browsing history_.
1. Click to confirm.
1. Pick the location in the repo as `imagescraper/var/history_raw/` and name as `edge.csv`.


## Filter history

Get relevant URLs out and write to a text file.

```sh
make chrome
make firefox
make edge
```

View the results as text files here: [imagescraper/var/browser_processed/](/imagescraper/var/browser_processed/).
