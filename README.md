Polygon Blockchain Monitor
==============

***Polygon Scan Scraper***

**Author:** *Bradley J.M.*

The goal of this program is to scrape all of the top market cap tokens' data from the Polygonscanner website. Then we will use the scraped data to populate a local database.

In the coming weeks, this program will be updated to monitor strong price performance and any new tokens breaking into the top tokens tracked by the polygonscanner's tokens' page. 
It will then email any new tokens', along with any unusually strong price performance to the subscribers. To subscribe please visit the CryptoFarmBets telegram/subreddit.

To gather the data and populate a local database, download all dependencies and then run either the execute.py file or the execute.ipynb.

This will populate a database in the project folder named 'Polygonscan' with a table titled 'poly{date}_{hour}'. The date will be formatted as YYMMDD and the hour will be formatted as HH.
