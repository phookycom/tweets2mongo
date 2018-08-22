import tweepy
import json
from pymongo import MongoClient
import argparse
import configparser

"""
Define some arguments (search words, database, collection and language) 
to run the script from console.
Usage example: python tweets2mongo.py -w#python -w#azure -w#aws  -d development -c cloudcomputing -l en
"""
parser = argparse.ArgumentParser()
parser.add_argument('-d','--database', help='<Required> Name of MongoDB Database (i.e. -d twitterdb)', required=True)
parser.add_argument('-c','--collection', help='<Required> Name of MongoDB collection (i.e. -c pythontweets)', required=True)
parser.add_argument('-w','--words', action='append', help='<Required> Keywords or hastags to filter the Twitter stream (i.e. -w#python)', required=True)
parser.add_argument('-l','--language', action='append', help='Language of tweets (i.e. -l en)', required=True)
args = parser.parse_args()
DATABASE = args.database
COLLECTION = args.collection
WORDS = args.words
LANGUAGES = args.language

MONGO_HOST= 'mongodb://localhost' #Define your MongoDB connection

KEYS_LOCATION = 'keys.conf' #Store your Twitter keys in a separate config file

class TwitterStream(tweepy.StreamListener):   

    def on_connect(self):
        # Function called to connect to the Twitter Streaming API
        print("You are now connected to the Twitter streaming API.")
 
    def on_error(self, status_code):
        # Function displays the error or status code
        print('An Error has occured: ' + repr(status_code))
        return False
 
    def on_data(self, data):
        #Function connects to the defined MongoDB and stores the filtered tweets
        try:
            #Connect to MongoDB host
            client = MongoClient(MONGO_HOST)

            #Use defined database (here: tweets)
            db = client[DATABASE]

            # Decode the JSON data from Twitter
            datajson = json.loads(data)
            
            #Pick the 'text' data from the Tweet
            tweet_message = datajson['text']

            #Show the text from the tweet we have collected
            print(tweet_message)
            
            #Store the Tweet data in the defined MongoDB collection
            db[COLLECTION].insert(datajson)
        except Exception as e:
           print(e)

def read_conf(settings_location):
    #Read the Twitter API keys from the keys file.
    
    settings = configparser.ConfigParser()
    settings.optionxform = str
    settings.read(settings_location)
    return settings

keys = read_conf(KEYS_LOCATION)['MAIN']
auth = tweepy.OAuthHandler(keys['CONSUMER_KEY'], keys['CONSUMER_SECRET'])
auth.set_access_token(keys['ACCESS_TOKEN'], keys['ACCESS_TOKEN_SECRET'])

#Initialize the Twitter listener.
listener = TwitterStream(api=tweepy.API(wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)
print("MongoDB database: " + str(DATABASE))
print("Database collection: " + str(COLLECTION))
print("Language: " + str(LANGUAGES))
print("Keywords: " + str(WORDS))
streamer.filter(track=WORDS, languages=LANGUAGES)