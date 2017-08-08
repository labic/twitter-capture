---
OVERVIEW
---

twitter-capture is a Python script for collecting and streaming tweets.

For collecting (REST API), multiple API keys can be used; for streaming,
authentication is required as of Twitter v1.1 (requires token key/secret).

Requires python3-twython library and credentials set in "config.py" file.

```
USAGE: twitter-capture.py [-h] [-v] -q QUERY
                          [-t {stream,terms,users,userids,ids,id}] [-l LANG]
                          [-g GEOCODE] [-n NUMBER] [-m MAX] [-s SINCE]
                          [-u URL] [-w WAIT] [--log LOG] [--nolog] [--nourl]
```

---
STARTING
---
Before running the script, it is required to set credentials in "config.py".
Other available settings are listed below:

```
APP_KEYS            array of API keys (for REST API)
                    [['api_key_1','api_secret_1'],['api_key_2','api_secret_2']]
APP_KEY             required for streaming and collecting (if APP_KEYS unset)
APP_SECRET          required for streaming and collecting (if APP_KEYS unset)
OAUTH_TOKEN         required for streaming only
OAUTH_TOKEN_SECRET  required for streaming only
POST_URL            API endpoint to send captured tweets to (default: None)
STREAM_RTS          enable or disable streaming retweets (default: True)
STREAM_ATS          enable or disable streaming @-messages (default: True)
```

---
RUNNING
---

For executing, only the QUERY argument is required. Available arguments:

```
-h, --help                       show help message and exit
-v, --version                    show program's version number and exit
-q QUERY, --query QUERY          query to search for (required)
-t TYPE, --type TYPE             input query type
                                   stream: stream live tweets
                                   terms: collect strings (default)
                                   users: collect timelines from user names
                                   userids: collect timelines from user IDs
                                   ids: collect a set of tweet IDs
                                   id: a single tweet ID
-l LANG, --lang LANG             language to search for
-g GEOCODE, --geocode GEOCODE    geocode location to search in
-n NUMBER, --number NUMBER       number of tweets to finish search
-m MAX, --max MAX                maximum tweet ID to capture
-s SINCE, --since SINCE          minimum tweet ID to capture
-u URL, --url URL                URL to send captured tweets to
-w WAIT, --wait WAIT             minutes to search again (default: OFF)
--log LOG                        output log file path
--nolog                          do NOT log script output
--nourl                          do NOT send tweets to endpoint
```

---
EXAMPLES
---

Stream tweets containing "#ForaTemer" in portuguese only:
```
twitter-capture.py -q "#ForaTemer lang:pt" -t stream
```

Capture tweets containing "Labic" in portuguese every 15 minutes:
```
twitter-capture.py -q "Labic" -l pt -w 15
```

Capture last 100 tweets from @ufeslabic timeline:
```
twitter-capture.py -q "@ufeslabic" -t users -n 100
```

List of available Twitter operators:
```
watching now          containing both 'watching' and 'now' (default)
“happy hour”          containing the exact phrase 'happy hour'
love OR hate          containing either 'love' or 'hate' (or both)
#haiku                containing the hashtag 'haiku'
from:alexiskold       sent from person 'alexiskold'
to:techcrunch         sent to person 'techcrunch'
@mashable             referencing person 'mashable'
since:2015-07-19      sent since date '2015-07-19'
until:2015-07-19      sent before the date '2015-07-19'
movie -scary          containing 'movie', but not 'scary'
cinema :)             containing 'cinema' and with a positive attitude
flight :(             containing 'flight' and with a negative attitude
traffic ?             containing 'traffic' and asking a question
cats filter:links     containing 'cats' and linking to URL
news source:web       containing 'news' and sent via website
```