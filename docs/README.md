# Image Scraper docs

- [Installation](installation.md)
    ```sh
    $ python -m venv venv
    $ source venv/bin/activate
    $ make all
    ```
- [Usage](usage.md)
    Quickstart without using any history files:
    ```sh
    $ make debug
    ```
    After you setup your browser history for one or more browsers:
    ```sh
    $ make chrome
    $ make firefox
    $ make edge

    $ make run
    ```
