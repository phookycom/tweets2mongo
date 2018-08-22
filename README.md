# tweets2mongo

### Description
A simple Python script to save tweets to a MongoDB using the Twitter Streaming API. Parameters can be used to pass the database, collection, language and keywords/hashtags in the terminal to the script.

### Prerequisites
You need the following Python packages:
* tweepy
* pymongo
* argparse
* configparser

To use the Twitter API you need your personal consumer key, consumer secret, access token and acces token secret. You can get it from the [Twitter Application Management](https://apps.twitter.com)

Rename *keys_default.conf* to *keys.conf* and put in the API keys. 


### Usage
`python tweets2mongo.py -w#python -w#azure -w#aws  -d development -c cloudcomputing -l en`

