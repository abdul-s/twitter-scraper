import settings
import json, csv, codecs
from operator import le,ge,eq
from datetime import datetime

from twitter import Twitter, OAuth, TwitterStream

class TweetWrapper:
    def create_auth(self):
        oauth = OAuth(settings.TWITTER_KEY, settings.TWITTER_SECRET, settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
        return oauth

    def get_data(self, track, count=10):
        twitter_stream = TwitterStream(auth=self.create_auth())
        iterator = twitter_stream.statuses.filter(track=track, language="en")
        return self.get_relevant_data(iterator, count)

    def get_relevant_data(self, iterator, count):
        tweets = []
        print "Getting data..."
        for tweet in iterator:
            if 'delete' in tweet:
                continue
            data = {}
            if tweet['truncated']:
                text = tweet['extended_tweet']['full_text']
            else:
                text = tweet['text']
            data['user_id'] = tweet['user']['id']
            data['user_id_str'] = tweet['user']['id_str']
            data['user_name'] = tweet['user']['screen_name'].encode('ascii', 'ignore')
            data['text'] = text.encode('ascii', 'ignore')
            data['location'] = tweet['user']['location'].encode('ascii', 'ignore') if tweet['user']['location'] is not None else None 
            data['created_at'] = datetime.strptime(tweet['created_at'],"%a %b %d %H:%M:%S +0000 %Y")
            data['friends_count'] = tweet['user']['friends_count']
            data['followers_count'] = tweet['user']['followers_count']
            data['retweet_count'] = tweet['retweet_count']
            tweets.append(data)
            if len(tweets) == count:
                break
        return tweets

    def export_csv(self, tweets, csv_name):
        with open(csv_name, "w") as file:
            csv_file = csv.writer(file)
            csv_file.writerow(['user_id', 'user_id_str', 'user_name', 'location', 'created_at', 'text', 'friends_count', 'followers_count', 'retweet_count'])
            for tweet in tweets:
                csv_file.writerow([tweet['user_id'], tweet['user_id_str'], tweet['user_name'], tweet['location'], tweet['created_at'], tweet['text'], tweet['friends_count'], tweet['followers_count'], tweet['retweet_count']])

    def text_filter(self, tweets, field, search_term):
        filtered_tweets = [tweet for tweet in tweets if search_term in tweet[field].strip().split(" ")]
        return filtered_tweets

    def number_filter(self, tweets, field, count, operation):
        if operation == 'less':
            op = le
        elif operation == 'greater':
            op = ge
        else:
            op = eq
        filtered_tweets = [tweet for tweet in tweets if op(int(tweet[field]),int(count))]
        return filtered_tweets         

    def date_filter(self, tweets, field, start_date, end_date):
        filtered_tweet = []
        start_date = datetime.strptime(start_date,"%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_date,"%Y-%m-%d %H:%M:%S")
        for tweet in tweets:
            tweet_date = tweet[field]
            if type(tweet[field]) != datetime:
                tweet_date = datetime.strptime(tweet[field],"%Y-%m-%d %H:%M:%S")
            if tweet_date >= start_date and tweet_date <= end_date:
                filtered_tweet.append(tweet)
        return filtered_tweet

    @staticmethod
    def read_csv_file(file_path, header = False):
        field_names = ['user_id', 'user_id_str', 'user_name', 'location', 'created_at', 'text', 'friends_count', 'followers_count', 'retweet_count']
        csvfile = codecs.open(file_path)
        reader = csv.DictReader(csvfile, field_names)
        if header:
            next(reader,None)
        rows = [ row for row in reader ]
        return rows