# MIGUEL MARTINEZ
# Put all import statements you need here.
import unittest
import itertools
import collections
import tweepy
import twitter_info
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

	return twitter_results

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
		baseurl = "http://www.omdbapi.com/?t="
		url = baseurl + name
		final_url = url.replace(" ","+")
		response = requests.get(final_url)
		omdb_results = json.loads(response.text)
		OMDB_CACHE_DICTION[unique_identifier] = omdb_results
		g = open(OMDB_CACHE_FNAME, 'w')
		g.write(json.dumps(OMDB_CACHE_DICTION))
		g.close()
	return omdb_results

## STAR CACHING BELOW TO ANALYZE JSON OBJECT
STAR_CACHE_FNAME = "SI206_finalproject_starcache.json"
try:
	star_cache_file = open(STAR_CACHE_FNAME,'r')
	star_cache_contents = star_cache_file.read()
	star_cache_file.close()
	STAR_CACHE_DICTION = json.loads(star_cache_contents)
except:
	STAR_CACHE_DICTION = {}

##Function to search star actor of movie
def star_actor_tweets(searchterm):
	unique_identifier = "star_{}".format(searchterm)
	if unique_identifier in STAR_CACHE_DICTION:
		print('using cached data for star', searchterm)
		star_results = STAR_CACHE_DICTION[unique_identifier]
	else:
		print('getting data from tweets from Twitter for star', searchterm)
		api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
		star_results = api.search(q = searchterm, count = 5)
		STAR_CACHE_DICTION[unique_identifier] = star_results
		r = open(STAR_CACHE_FNAME, 'w')
		r.write(json.dumps(STAR_CACHE_DICTION))
		r.close()
	return star_results
#Invoking to test cache files

wizard_oz = get_movie_cache("The Wizard of Oz")
umich = get_twitter_cache("umich")
actor = star_actor_tweets("Judy Garland")



#Class Setup
class Movie():
	def __init__(self, movie_dict={}):
		self.imdbID = movie_dict['imdbID']
		self.title = movie_dict['Title']
		self.director = movie_dict['Director']
		self.imdb_rating = movie_dict['imdbRating']
		self.actors = movie_dict['Actors'].split(',')
		self.language = len(movie_dict['Language'].split())

	def __str__(self):
		return "{} was directed by {} and received an aggregate score of {} on IMBD".format(self.title, self.director, self.imdb_rating)

class TwitterUser():
	def __init__(self, tweet_dict):
		self.screen_name = tweet_dict[0]['user']['screen_name']
		self.id = tweet_dict[0]['user']['id']
		self.favourites_count = tweet_dict[0]['user']['favourites_count']
		
	
## FINISH CLASS TWEET
#class Tweet():
#	def __init__(self, tweet_dict):
	#	if 'text'


#Class invocation
wizard_class = Movie(wizard_oz)
twitteruser_class = TwitterUser(umich)


#Database file setup
conn = sqlite3.connect('206_finalproject.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('DROP TABLE IF EXISTS Movies')
cur.execute('CREATE TABLE Tweets (tweet_id TEXT PRIMARY KEY, text TEXT, screen_name TEXT, movie_title TEXT, num_favs INTEGER, retweets INTEGER, FOREIGN KEY (screen_name) REFERENCES Users(screen_name), FOREIGN KEY (movie_title) REFERENCES Movies(movie_title))')
cur.execute('CREATE TABLE Users (user_id TEXT PRIMARY KEY, screen_name TEXT, num_favs INTEGER)')
cur.execute('CREATE TABLE Movies (movie_id TEXT PRIMARY KEY, movie_title TEXT, director TEXT, num_languages INTEGER, imdb_rating INTEGER, top_actor TEXT)')

#Adding data to User table
cur.execute("INSERT INTO Users (user_id, screen_name, num_favs) VALUES (?, ?, ?)", (twitteruser_class.id, twitteruser_class.screen_name, twitteruser_class.favourites_count))
conn.commit()

#Adding data to Movie table
cur.execute("INSERT INTO Movies (movie_id, movie_title, director, num_languages, imdb_rating, top_actor) VALUES (?, ?, ?, ?, ?, ?)", (wizard_class.imdbID, wizard_class.title, wizard_class.director, wizard_class.language, wizard_class.imdb_rating, wizard_class.actors[0]))
conn.commit()

#Adding data to Tweets table:


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
		wizard_class = Movie(wizard_oz)
		self.assertEqual(type(wizard_class.__str__()), type(""), "testing type of __str__ method, should be str")
	def test_num_languages(self):
		wizard_class = Movie(wizard_oz)
		self.assertEqual(wizard_class.language, 1, "testing that wizard of oz has 1 language")
	def test_users_table(self):
		conn = sqlite3.connect('206_finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result)>=1, "Testing there is at least 1 user in the User table")
	def test_tweets_table(self):
		conn = sqlite3.connect('206_finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==6, "Testing that there are 6 columnns in the Tweets table")
	def test_movies_table(self):
		conn = sqlite3.connect('206_finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==6, "Testing that there are 6 columns in the Movies table")
	def test_top_billed(self):
		wizard_class = Movie(wizard_oz)
		self.assertTrue("Judy Garland" in wizard_class.actors, "Testing that Judy Garland is correctly in the actors list for the Wizard of Oz movie")

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
	unittest.main(verbosity=2)