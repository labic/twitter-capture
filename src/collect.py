#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Collect tweets by text, tweet IDs, user names, user IDs or geocode location.

Query input might be empty if coordinates are given as in:
	'latitude,longitude,radius' eg. '-20.3,-40.1,100km'

Accepts multiple API keys in the following format:
	[['api_key_1','api_secret_1'],['api_key_2','api_secret_2']]

Accepts different query types:
	'terms' - strings such as words and hashtags
	'users' - timelines from user names
	'userids' - timelines from user IDs
	'ids' - a set of tweet IDs
	'id' - a single tweet ID

More information on query operators can be read at:
	https://dev.twitter.com/rest/public/search
"""

from os.path import isfile
# from twython import Twython, TwythonError
from twython import TwythonRateLimitError

from config import APP_KEYS
from .api import auth_twitter, post_tweets, sleep_seconds

try: # import JSON lib
	import json
except ImportError:
	import simplejson as json

def collect(query, query_type='terms', lang=None, geocode=None, max_id=None, since_id=None,
			stop_number=None, post_url=None, wait_time=None, separator=None):

	from_date = None # last captured date
	maximum = None # last captured ID
	current = 0 # number of current ongoing query
	total = 0 # number of total tweets captured
	tts = 900 # time to sleep if error on endpoint
	count = 100 # number of tweets in each query

	count = stop_number if isinstance(stop_number, int)\
						and stop_number < count else count

	# read from file
	if isfile(query):
		query_strings = []
		print('Loading query from file...')
		with open(query, 'rt', encoding='utf8') as f:
			next(f) # skip header
			for line in f:
				query_strings.append(line.rstrip('\n'))
		query = query_strings

	if isinstance(query, str):
		if separator: # split query
			query = query.replace(separator+' ',separator).split(separator)
		else: query = [query] # single

	int_len_query = len(query)

	# log in Twitter
	print('Authenticating...')
	twitter = auth_twitter(APP_KEYS)

	# split input IDs
	if query_type == 'ids':
		print('Collecting', int_len_query, 'IDs...')
		query = split_list(query, 100)

	while True:
		for q in query:
			current += (len(q) if query_type == 'ids' else 1)
			captured = 0 # number of tweets captured in this query
			first_id = None # first captured ID for future searches
			maximum = max_id # oldest tweet to finish capturing
			minimum = since_id # most recent tweet to start capturing
			previous_results = None # compare returned output
			search_results = None # returned output itself

			# print current query being made
			if query_type in ('terms', 'users', 'userids'):
				print('\nCollecting', ('"' + q + '"' if query_type == 'terms' else ('@' + q + ' timeline')),
					  '(' + str(current) + '/' + str(len(query)) + ')...')

			while True: # keep searching
				try: # collecting
					if query_type == 'terms':
						search_results = twitter.search(q=q,
												count=count,
												lang=lang,
												max_id=maximum,
												since_id=minimum,
												geocode=geocode)
						print(minimum, maximum)
						search_results = search_results['statuses']

					elif query_type == 'users':
						search_results = twitter.get_user_timeline(screen_name=q,
														   count=count,
														   max_id=maximum,
														   since_id=minimum)

					elif query_type == 'userids':
						search_results = twitter.get_user_timeline(user_id=q,
														   count=count,
														   max_id=maximum,
														   since_id=minimum)

					elif query_type == 'ids':
						search_results = twitter.lookup_status(id=q)

					elif query_type == 'id':
						search_results = twitter.show_status(id=q)
						search_results = [search_results]

					for some_results in split_list(search_results, 10):
						tweets = [] # array to store and send tweets

						for status in some_results:
							captured += 1 # tweets captured in this query
							total += 1 # tweets captured in all queries
							first_id = status['id'] if captured == 1 else fist_id
							from_date = status['created_at'].replace(' +0000','')
							maximum = (status['id'] - 1)
							tweet = json.dumps(status)
							tweets.append(tweet)

						if post_url: # send to API endpoint
							post_tweets(tweets, post_url)

					if not search_results\
					or captured == stop_number\
					or search_results == previous_results\
					or max_id and int(maximum) >= int(max_id)\
					or since_id and int(minimum) <= int(since_id)\
					or (current == int_len_query and query_type in ('ids', 'id')):
						break

					print('Got', captured, 'tweets. Last:', from_date, 'ID:', maximum)
					previous_results = search_results

				except TwythonRateLimitError:
					twitter = auth_twitter(APP_KEYS, query_type)

				except KeyboardInterrupt:
					print('Finishing...')
					break

				# except Exception as e:
					# print('Warning:', e)
					# if ('429 (Too Many Requests)' in str(e)):
					# 	twitter = auth_twitter(api_keys, query_type)
					# elif any([s in str(e) for s in ('404 (Not Found)', '401 (Unauthorized)')]):
					# 	break

				if query_type in ('ids', 'id'):
					break

			print('\nGot', captured, 'tweets.\nLast:', from_date, '\nMax ID:', maximum)

		if int_len_query > 1:
			print('\nGot', total, 'total tweets.')

		if isinstance(wait_time, int):
			since_id = first_id
			sleep_seconds(wait_time)
		else: break

def split_list(iterable, chunksize=100):
	'''
	Split an array in iterables of N items.
	'''
	for i,c in enumerate(iterable[::chunksize]):
		yield iterable[i*chunksize:(i+1)*chunksize]