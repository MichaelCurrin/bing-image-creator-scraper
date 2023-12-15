# Browser history

## Firefox

1. Go to this directory in Windows. Note that `AppData` is usually hidden so it's best to enter this path in your file browser.
    ```
    C:\Users\<username>\AppData\Roaming\Mozilla\Firefox\Profiles
    ```
1. Find the relevant directory for your profile and go into it.
1. Find the `places.sqlite` file.
1. Copy that file into this repo in the `imagescraper/var/browser_raw` directory.
1. Get relevant URLs out and write to a text file using this command:
    ```sh
    make firefox
    ```
1. View the output file here:
    ```
    imagescraper/var/browser_processed/firefox_urls.txt
    ```

## Edge

1. Go to History (<kbd>CTRL</kbd>+<kbd>H</kbd>).
1. click the menu (three dots).
1. Click _Export browsing history_.
1. Click to confirm, pick a location.
