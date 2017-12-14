# Twitter Scraper

Scrape tweets from twitter into csv file.
Filter downloaded csv

## Installation

* `pip install -r requirements.txt`

## Setup

* Sign up for a Twitter [developer account](https://dev.twitter.com/).
* Create an application [here](https://apps.twitter.com/).
* Set the following keys in `settings.py`.  You can get these values from the app you created:
    * `TWITTER_KEY`
    * `TWITTER_SECRET`
    * `TWITTER_APP_KEY`
    * `TWITTER_APP_SECRET`

## Usage: 
* tweets.py console [--track=<text>] [--limit=<limit>]
* tweets.py export --file-out=<filename.csv> [--track=<text>] [--limit=<limit>]
* tweets.py filterSavedData --file-in=<filename.csv> --field-name=<text> --text-search=<keyword> [--file-out=<filename.csv>]
* tweets.py filterSavedData --file-in=<filename.csv> --field-name=<text> --start-date=<date> --end-date=<date> [--file-out=<filename.csv>]
* tweets.py filterSavedData --file-in=<filename.csv> --field-name=<text> --number=<number> --operator=<less|greater|equal> [--file-out=<filename.csv>]
* tweets.py -h | --help

### Options:
* --track=<text>     .				Search text  [Default: Apple].
* --limit=<limit>					Optional parameter Number of tweet to retrive  [Default: 10].
* --file-out=<filename.csv>			CSV Filename.
* --file-in=<filename.csv>			CSV Filename.
* --field-name=<text>				Only Supported fields
* --start-date=<date>				Date in %Y %m %d %H:%M:%S format
* --end-date=<date>				Date in %Y %m %d %H:%M:%S format
* --number=<number>				Number for query
* --operator=<less|greater|equal>			Operator to use for comparison
* -h --help               			Show this screen.
