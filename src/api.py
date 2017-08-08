#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Authenticate using Twitter's credentials as in 'config.py'.

Query types have different limits every 15 minute window:
	'terms': 450 requests (100 tweets/request);
	'users': 1500 requests (100 tweets/request);
	'userids': same as above, no change;
	'ids': 300 requests (100 tweets/request);
	'id': 900 requests (1 tweet/request);
	'trends': 75 requests (1 region/request).

More information on API rate limits can be found at:
	https://dev.twitter.com/rest/public/rate-limits
"""

from datetime import datetime
from requests import post
from time import time, sleep
from twython import Twython, TwythonRateLimitError

def auth_twitter(app_keys, query_type='terms'):
	if query_type == 'terms':
		resource = ['search', '/search/tweets']
	elif query_type in ('users', 'userids'):
		resource = ['statuses', '/statuses/user_timeline']
	elif query_type == 'ids':
		resource = ['statuses', '/statuses/lookup']
	elif query_type == 'id':
		resource = ['statuses', '/statuses/show/:id']
	elif query_type == 'trends':
		resource = ['trends', '/trends/place']

	remaining = 0
	len_app_keys = len(app_keys)

	while True:
		tts = 900
		rate_limit_exceeded = False

		for key in app_keys:
			try: # authenticate
				twitter = Twython(key[0], key[1], oauth_version=2)
				access_token = twitter.obtain_access_token()
				twitter = Twython(key[0], access_token=access_token)
				rate_limit_status = twitter.get_application_rate_limit_status(resources=resource[0])
				rate_limit_status = rate_limit_status['resources'][resource[0]][resource[1]]
				remaining = rate_limit_status['remaining']
				limit = rate_limit_status['limit']
				reset = rate_limit_status['reset'] - time() + 1

				if remaining > 0:
					print('Requests left:', str(remaining) + '/' + str(limit),
						  '(' + str(app_keys.index(key)+1) + '/' + str(len_app_keys) + ')')
					return twitter

				elif tts > reset:
					tts = reset

			except TwythonRateLimitError:
				rate_limit_exceeded = True

			except Exception as e:
				print('Warning:', e)

		if remaining == 0:
			print('Warning: 0 requests left.')\
				if rate_limit_exceeded else None
			sleep_seconds(tts)

def post_tweets(array, url):
	'''
	Send tweets array to API endpoint.
	'''
	while True: # try until succeeded
		response = post(url, json=array)
		if '200' not in str(response):
			print('\nWarning: error sending tweets to API endpoint.')
			sleep_seconds(tts)
		else: break

def sleep_seconds(tts):
	'''
	Sleep for a given amount of seconds.
	'''
	ttw = datetime.fromtimestamp(int(time() + tts))
	ttw = datetime.strftime(ttw, "%H:%M:%S")
	print('Sleeping', str(int(tts)) + 's until', ttw + '.')
	for i in range(3):
		sleep(0.5)
		print('.')
	sleep(tts)