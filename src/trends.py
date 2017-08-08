#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Get a list of current trending topics on Twitter according
to country name, code or WOEID (imported from "lib_woeid.py").

Accepts multiple API keys in the following format:
	[['api_key_1', 'api_secret_1'],['api_key_2','api_secret_2']]

TO DO: send trending topics to API endpoint in an ordered fashion.
"""

from collections import defaultdict
from .api import auth_twitter
from .woeid import WHERE_ON_EARTH
from config import APP_KEYS

def trending_topics(query, post_url=None, show_all_topics=False):
	try: # check if WOEID
		query = int(query)

	except ValueError: # search for string
		query = 'global' if query == '' else query
		query = ('(' + query.upper() + ')') if len(query) == 2 else query

		for key in WHERE_ON_EARTH.keys():
			if query.lower() in key.lower():
				query = WHERE_ON_EARTH.get(key)
				break

	twitter = auth_twitter(APP_KEYS, 'trends') # get Twitter credentials
	trending = twitter.get_place_trends(id=query) # get trending topics
	trending_topics = defaultdict(int) # set it as dictionary

	for topic in trending[0]['trends']:
		if topic['tweet_volume']: # add to dictionary
			trending_topics[topic['name']] += topic['tweet_volume']
		elif show_all_topics: # tweet count is None
			trending_topics[topic['name']] = 0

	# sort TTs
	ordered_list = []
	for keys, value in trending_topics.items():
		ordered_list.append([keys, value])
	ordered_list = sorted(ordered_list, key=lambda t: t[1], reverse=True)

	# print TTs
	count_topics = 0
	print('Trending topics on', trending[0]['locations'][0]['name'] + ':')
	for line in ordered_list:
		count_topics += 1
		try: print(str(count_topics) + ':', line[0], '-', line[1], 'tweets.')
		except: print(str(line[0]).encode('utf8', 'ignore').decode('ascii', 'ignore'),
					  '-', line[1], 'tweets.')