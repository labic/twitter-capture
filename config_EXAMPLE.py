#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module sets user credentials for Twitter collecting
and streaming, as well as the API URL for sending tweets.

The APP_KEYS var is imported for collecting already published
tweets, while the vars APP_KEY, APP_SECRET, OAUTH_TOKEN and
OAUTH_TOKEN_SECRET are imported for streaming live tweets.

The POST_URL var is used for sending the obtained tweets over
to an external API endpoint, and becomes the default if set.
However, if another URL is given on execution time with the
"--url" argument, the former will be ignored for the latter.
"""

# APP_KEYS = [ # array of arrays
	# ['MY_FIRST_APP_KEY', 'MY_FIRST_APP_SECRET'],
	# ['MY_SECOND_APP_KEY', 'MY_SECOND_APP_SECRET']]

# APP_KEY = 'MY_TWITTER_APP_KEY'
# APP_SECRET = 'MY_TWITTER_APP_SECRET'
# OAUTH_TOKEN = 'MY_TWITTER_TOKEN_KEY'
# OAUTH_TOKEN_SECRET = 'MY_TWITTER_TOKEN_SECRET'

# POST_URL = 'https://inep-api-v2-dev.herokuapp.com/v2/tweets'

# LOG_OUTPUT = False # default: True
# STREAM_RTS = False # retweets, default: True
# STREAM_ATS = False # @-messages, default: True