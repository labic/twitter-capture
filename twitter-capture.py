#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Read arguments given on script execution and start
collecting or streaming tweets according to input.

Credentials are imported by collect() and stream()
and must be as instructed in "config.py" file.

If the POST_URL var is in "config.py", it becomes
the default API URL to send captured tweets to. If
however an URL is on execution with the "--url"
argument, it will override the imported default.

The "--noapi" argument is for testing purposes and
sets the script to print captured output only.
"""

__url__ = 'http://github.com/Labic/twitter-capture'
__version__ = '0.1'

import sys

from argparse import ArgumentParser, RawTextHelpFormatter
from os import getpid, mkdir
from os.path import abspath, dirname, exists, realpath
from src.collect import collect
from src.logger import Logger
from src.stream import stream
# from src.trends import trending_topics
from time import time

try: from config import POST_URL
except: POST_URL = None

try: from config import LOG_OUTPUT
except: LOG_OUTPUT = True

if __name__ == '__main__':

	log_path = dirname(realpath(sys.argv[0])) + '/log/'
	log_file = log_path + str(int(time())) + '_' + str(getpid()) + '.txt'

	parser = ArgumentParser()
	parser.add_argument('-v', '--version', action='version', version=__version__)
	parser.add_argument('-q', '--query', action='store', help='query to search for', required=True)
	parser.add_argument('-t', '--type', action='store', help='input query type',
						default='terms', choices=['stream', 'terms', 'users', 'userids', 'ids', 'id']) # 'trends'])
	parser.add_argument('-l', '--lang', action='store', help='language to search for')
	parser.add_argument('-g', '--geocode', action='store', help='geocode location to search in')
	parser.add_argument('-n', '--number', action='store', type=int, help='number of tweets to finish search')
	parser.add_argument('-m', '--max', action='store', type=int, help='maximum tweet ID to finish searching')
	parser.add_argument('-s', '--since', action='store', type=int, help='minimum tweet ID to start searching')
	parser.add_argument('-u', '--url', action='store', help='URL to send captured tweets to', default=POST_URL)
	parser.add_argument('-w', '--wait', action='store', type=int, help='minutes to search again (default: OFF)')
	parser.add_argument('--log', action='store', help='output log file path', default=log_file if LOG_OUTPUT else False)
	parser.add_argument('--nolog', action='store_const', const=False, help='do NOT log script output', dest='log')
	parser.add_argument('--nourl', action='store_const', const=None, help='do NOT send tweets to endpoint', dest='url')

	# parse command line arguments
	args = parser.parse_args()
	dict_args = vars(args)

	# print arguments
	for k in dict_args:
		print(k, '=', dict_args[k])
	print() # jump line

	if args.log: # start logging system output
		log_file = abspath(args.log)
		mkdir(log_path) if not exists (log_path) else None
		sys.stdout = sys.stderr = sys.stdin = Logger(log_file, 'a')

	if args.type == 'stream':
		stream(query=args.query,
			   post_url=args.url)

	# elif args.type == 'trends':
	# 	trending_topics(query=args.query,
	# 					post_url=args.url)

	else: # get published tweets
		collect(query=args.query,
				query_type=args.type,
				lang=args.lang,
				geocode=args.geocode,
				max_id=args.max,
				since_id=args.since,
				stop_number=args.number,
				post_url=args.url,
				wait_time=args.wait,
				separator=',')