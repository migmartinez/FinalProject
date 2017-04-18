###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# MIGUEL MARTINEZ
# Put all import statements you need here.
import unittest
import itertools
import collections
import tweepy
import twitter_info # same deal as always...
import json
import sqlite3
import re
from collections import Counter
import sys
import codecs
import requests
import omdb

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

# Begin filling in instructions....
## Tweepy setup below to cache twitter data, make sure that twitter_info file is present in directory.
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

## END TWEEPY SET UP CODE
## TWITTER CACHING BELOW
TWITTER_CACHE_FNAME = "SI206_finalproject_twittercache.json"
try:
	twitter_cache_file = open(TWITTER_CACHE_FNAME,'r')
	twitter_cache_contents = twitter_cache_file.read()
	twitter_cache_file.close()
	TWITTER_CACHE_DICTION = json.loads(twitter_cache_contents)
except:
	TWITTER_CACHE_DICTION = {}

## Function to get user tweets from user Twitter handle.
def get_twitter_cache(handle):
	unique_identifier = "twitter_{}".format(handle)
	if unique_identifier in TWITTER_CACHE_DICTION:
		print('using cached data for Twitter user', handle)
		twitter_results = TWITTER_CACHE_DICTION[unique_identifier]
	else:
		print('getting data from internet for Twitter user', handle)
		twitter_results = api.user_timeline(handle)
		TWITTER_CACHE_DICTION[unique_identifier] = twitter_results
		f = open(TWITTER_CACHE_FNAME,'w')
		f.write(json.dumps(TWITTER_CACHE_DICTION))
		f.close()

	twenty_tweets = []
	for tweet in twitter_results:
		twenty_tweets.append(tweet)
	return twenty_tweets[:20]

## OMBD CACHING BELOW
OMDB_CACHE_FNAME = "SI206_finalproject_OMBDcache.json"
try:
	omdb_cache_file = open(OMDB_CACHE_FNAME,'r')
	omdb_cache_contents = omdb_cache_file.read()
	omdb_cache_file.close()
	OMDB_CACHE_DICTION = json.loads(omdb_cache_contents)
except:
	OMDB_CACHE_DICTION = {}

## Function to get movie data from OMBD movie title
def get_movie_cache(name):
	unique_identifier = "omdb_{}".format(name)
	if unique_identifier in OMDB_CACHE_DICTION:
		print('using cached data for movie', name)
		omdb_results = OMDB_CACHE_DICTION[unique_identifier]
	else:
		print('getting data from internet for movie', name)
		omdb_results = omdb.search_movie(name)
		OMDB_CACHE_DICTION[unique_identifier] = omdb_results
		g = open(OMDB_CACHE_FNAME, 'w')
		g.write(json.dumps(OMDB_CACHE_DICTION))
		g.close()


#Invoking 

wizard_oz = get_movie_cache("The Wizard of Oz")
umich = get_twitter_cache("umich")
# Put your tests here, with any edits you now need from when you turned them in with your project plan.
class Task1(unittest.TestCase):
	def test_twitter_cache(self):
		f = open("SI206_finalproject_twittercache.json", "r")
		s = f.read()
		f.close()
		self.assertEqual(type(s),type(""), "Caching is not working correctly for twitter")
	def test_OMBD_cache(self):
		f = open("SI206_finalproject_OMBDcache.json", "r")
		s = f.read()
		f.close()
		self.assertEqual(type(s), type(""), "Caching is not working correctly for OMBD")
	def test_movie_str(self):
		m = Movie("The Wizard of Oz")
		self.asssertEqual(type(m.__str__()), type(""), "testing type of __str__ method, should be str")
	def test_num_languages(self):
		m = Movie("The Wizard of Oz")
		self.assertEqual(m.find_languages(), 1, "testing that wizard of oz has 1 language")
	def test_users_table(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result)>=1, "Testing there is at least 1 user in the User table")
	def test_tweets_table(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==6, "Testing that there are 6 columnns in the Tweets table")
	def test_movies_table(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==6, "Testing that there are 6 columns in the Movies table")
	def test_top_billed(self):
		m = Movie("The Wizard of Oz")
		self.assertTrue("Judy Garland" in m.actors, "Testing that Judy Garland is correctly in the actors list for the Wizard of Oz movie")

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
	unittest.main(verbosity=2)