Polygon Blockchain Monitor
==============

***Polygon Scan Scraper***

**Author:** *Bradley J.M.*

The goal of this program is to scrape all of the top market cap tokens' data from the https://polygonscan/tokens website. This program will email the new tokens and the tokens with the strongest price performance to everyone on the email list.

To gather the data and populate a local database, download all dependencies and then run the runScraper.py file or the runScraper.ipynb file. This will populate a local SQL database, 'polygonscan.db', with a table titled 'poly{date}_{hour}'. The date will be formatted as yyMMDD and the hour will be formatted as HH. Each subsequent download will be added to the .db file as it's own table, so long as the hour has changed by at least 1, otherwise it will overwrite the previous table.
