#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Stream tweets by keywords and send to API.

Requires API key/secret and token key/secret.

More information on query operators can be read at:
	https://dev.twitter.com/rest/public/search
"""

from requests import post
from twython import TwythonStreamer
from config import APP_KEY, APP_SECRET
from config import OAUTH_TOKEN, OAUTH_TOKEN_SECRET

from .api import post_tweets

try: # import JSON lib
	import json
except ImportError:
	import simplejson as json

try: # capture @-messages
	from config import STREAM_ATS
except: STREAM_ATS = True

try: # capture retweets
	from config import STREAM_RTS
except: STREAM_RTS = True

class Stream(TwythonStreamer):
	'''
	Execute action on every streamed tweet.
	'''
	def on_success(self, data):
		if 'text' in data:
			load_tweet(data)

	def on_error(self, status_code, data):
		print(status_code, data)
		return True # don't quit streaming
		# self.disconnect() # quit streaming

	def on_timeout(self):
		print >> sys.stderr, 'Timeout...'
		return True # don't quit streaming

def stream(query, post_url):
	'''
	Start streaming tweets.
	'''
	global API_URL, TWEETS

	API_URL = post_url # URL to send tweets
	TWEETS = [] # array for sending tweets

	print('Authenticating...')
	# requires authentication as of Twitter API v1.1
	stream = Stream(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

	print('Streaming...\n\nTweets: True\nRetweets: '+str(STREAM_RTS)+'\n@-messages: '+str(STREAM_ATS)+'\n')
	stream.statuses.filter(track=query)
	# stream.site(follow='twitter')
	# stream.user()

def print_tweet(data):
	'''
	Print captured tweet on terminal screen.
	'''
	tweet_text = data['text'].encode('utf8', 'ignore').decode('ascii', 'ignore').replace("\n", "")
	tweet_username = '@' + data['user']['screen_name']
	print(tweet_username, str(' ')*int(20-len(tweet_username)), tweet_text, '(' + data['id_str'] + ')')

def load_tweet(data):
	'''
	Store tweet to array in JSON format.
	'''
	is_at = True if data['in_reply_to_status_id'] else False # tweet_text.startswith('@')
	is_rt = True if 'retweeted_status' in data else False # tweet_text.startswith('RT @')
	is_tweet = all(not i for i in [is_at, is_rt])

	if is_tweet or (is_at and STREAM_ATS) or (is_rt and STREAM_RTS):
		print_tweet(data)
		tweet = json.dumps(data)
		TWEETS.append(tweet)

	if len(TWEETS) == 10:
		send_tweets()
		reset_tweets()

def send_tweets():
	'''
	Send tweets array to API endpoint.
	'''
	post_tweets(TWEETS, API_URL)

def reset_tweets():
	'''
	Reset tweets array after successful post.
	'''
	global TWEETS
	TWEETS = []