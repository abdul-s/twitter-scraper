#!/usr/bin/env python2
"""

Usage: 
tweets.py console [--track=<text>] [--limit=<limit>]
tweets.py export --file-out=<filename.csv> [--track=<text>] [--limit=<limit>]
tweets.py filterSavedData --file-in=<filename.csv> --field-name=<text> --text-search=<keyword> [--file-out=<filename.csv>]
tweets.py filterSavedData --file-in=<filename.csv> --field-name=<text> --start-date=<date> --end-date=<date> [--file-out=<filename.csv>]
tweets.py filterSavedData --file-in=<filename.csv> --field-name=<text> --number=<number> --operator=<less|greater|equal> [--file-out=<filename.csv>]
tweets.py -h | --help

Options:
--track=<text>     .				Search text  [Default: Apple].
--limit=<limit>					Optional parameter Number of tweet to retrive  [Default: 10].
--file-out=<filename.csv>			CSV Filename.
--file-in=<filename.csv>			CSV Filename.
--field-name=<text>				Only Supported fields
--start-date=<date>				Date in %Y %m %d %H:%M:%S format
--end-date=<date>				Date in %Y %m %d %H:%M:%S format
--number=<number>				Number for query
--operator=<less|greater|equal>			Operator to use for comparison
-h --help               			Show this screen.
"""
import sys,traceback
from docopt import docopt
from datetime import datetime

from twitterAPI import TweetWrapper 

def run(arguments): 
    track = arguments['--track']
    max_tweets = parse_max_tweets(arguments['--limit'])
    try:
		tweet = TweetWrapper()
		if arguments['console']:
			tweets = tweet.get_data(track=track, count=max_tweets)
			print_tweet(tweets)
		elif arguments['export']:
			file_name = arguments['--file-out']
			tweets = tweet.get_data(track=track, count= max_tweets)
			tweet.export_csv(tweets, file_name)
		elif arguments['filterSavedData']:
			filter_tweet = []
			file_out = arguments['--file-out']
			file_in = arguments['--file-in']
			field = arguments['--field-name']
			rows = TweetWrapper.read_csv_file(file_in, header=True)
			if arguments['--text-search'] is not None:
				keyword = arguments['--text-search']
				filter_tweet = tweet.text_filter(rows, field, keyword)
			elif arguments['--start-date'] is not None and arguments['--end-date'] is not None:
				start_date = arguments['--start-date']
				end_date = arguments['--end-date']
				filter_tweet = tweet.date_filter(rows, field, start_date, end_date)
			elif arguments['--number'] is not None:
				count = arguments['--number']
				operator = arguments['--operator']
				print count, operator
				filter_tweet = tweet.number_filter(rows, field, count, operator)
			if file_out is not None:
				tweet.export_csv(filter_tweet, file_out)
			else:
				print_tweet(filter_tweet)
		else:
			print "Unknown Option"
    except Exception:
        traceback.print_exc()
        sys.exit(1)

def parse_max_tweets(max_tweets):
    try:
        return int(max_tweets)
    except:
        print('max-tweets must be a number')
        sys.exit(1)

def print_tweet(tweets):
	if len(tweets) != 0:
		for t in tweets:
			print t
	else:
		print "No result found"

def parse_date(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        return True
    except ValueError:
        print('date must be specified as yyyy-mm-dd')
        sys.exit(1)

if __name__ == '__main__':
    arguments = docopt(__doc__)
    run(arguments)