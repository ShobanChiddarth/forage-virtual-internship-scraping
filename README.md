# Scraping Job Data from Virtual Internships on Forage

Selenium Python script to scrape job data from forage virtual internships.

### Requirements
1. Python 3.12.3
2. Modules on [requirements.txt](./requirements.txt)
3. Chromium driver

### Setup
1. Create virtual environment
2. `pip install -r requirements.txt`
3. Get chromium driver for your system and put it in PATH. 
4. Edit the `create_driver` function in [main.py](./main.py) to match your system's chromium driver configurations
5. Copy the file [input-links-sample.txt](./input-links-sample.txt) into `input-links.txt`
6. Go to forage and get the links of the virtual internships you want to scrape and paste the links to those jobs line by line
7. Run the script, do not touch your mouse and keyboard, and wait for it to complete.
8. After it is completed, you will get a new file `output.json` which has the data.
9. You can move it to the folder `outputs-archive` with a different name and timestamp if you want to store it

This file [2026-03-02-03-50-cybersecurity-jobs-scraped.json](./2026-03-02-03-50-cybersecurity-jobs-scraped.json) has the output you'll get for the links in [input-links-sample.txt](./input-links-sample.txt)
