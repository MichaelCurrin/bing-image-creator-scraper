# Bing Image Creator Scraper
> Bulk-download your AI images and prompts created with Bing, based on relevant URLs you provide from your browser history

[![OS - Linux](https://img.shields.io/badge/OS-Linux-blue?logo=linux&logoColor=white)](https://www.linux.org/ "Go to Linux homepage")
[![Made with Python](https://img.shields.io/badge/Python->=3.6-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")
[![GitHub tag](https://img.shields.io/github/tag/MichaelCurrin/bing-image-creator-scraper?include_prereleases=&sort=semver&color=blue)](https://github.com/MichaelCurrin/bing-image-creator-scraper/releases/)


## How it works

1. Make creations with Bing Image Creator.
1. Go through each browser (Firefox and Edge) on each computer where you use Bing Image Creator to create images and export the history.
1. Provide the history files to this app and it will extract only the relevant URLs. _Note the app does not care about your history besides URLS containing the Bing domain, so your history is kept private - see [Makefile](/Makefile)._
1. Then you scrape with this Python tool to get all the prompts and images downloaded. That you should cover everything you ever created (as long as you didn't clear your history and nothing expired on Bing's side).

### Can I get all images?

You are **not** guaranteed to get all images. Whether you use this scraper or navigate directly in the browser, some of the images appear as not available. It seems like Bing removes older creations from its storage. You can of course use the prompt to make new images which are close to the ones that you made before._

From _Frequently asked questions_ on the creations page, "Your images will be stored for up to 90 days". So use this tool to get them now!


## Documentation

For info on Bing Image Creator and this app's installation and usage instructions, see the docs.

<div align="center">

[![view - Documentation](https://img.shields.io/badge/view-Documentation-blue?style=for-the-badge)](/docs/ "Go to project documentation")

</div>


## License

No license is provided - this repo is closed for reuse and sharing of code except by anyone added as a collaborator.

Use of this tool is at your own risk and this tool provides no guarantee or warranty or protection around the scraping process or what you do with the images. Be responsible - see the section below.


## Is web scraping legal?

### Your own iamges

This tool is intended for ethical and legal scraping of your **own** creations. So you can use them as you like.

From [Image Creator Terms of Use](https://www.bing.com/new/termsofuseimagecreator?FORM=GENTOS)

> Microsoft does not claim ownership of Prompts, Creations, or any other content you provide, post, input, or submit to, or receive from, Image Creator (including feedback and suggestions).

### Images by other users

If you use this tool to scrape content that someone sent you by URL or browsed via the _Explore ideas_ tab, you do **not** have ownership of those so you may **not** use those images. 

Copyright law protects the original works of authorship of authors, including photographs. Therefore, you must obtain permission from the individual users who created the images you want to scrape before using them for any purpose other than personal use. This includes using them for commercial purposes, distributing them publicly, or embedding them in other websites or applications.

The prompts though are made public on the Creations page so you are welcome to reuse a prompt from another user.
