# MIGUEL MARTINEZ
# SI 206 Final Project
# Import Statements:

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
import datetime


sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

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

## Function to get tweets from Twitter handle.
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
OMDB_CACHE_FNAME = "SI206_finalproject_OMDBcache.json"
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

## STAR CACHING BELOW 
STAR_CACHE_FNAME = "SI206_finalproject_starcache.json"
try:
	star_cache_file = open(STAR_CACHE_FNAME,'r')
	star_cache_contents = star_cache_file.read()
	star_cache_file.close()
	STAR_CACHE_DICTION = json.loads(star_cache_contents)
except:
	STAR_CACHE_DICTION = {}



# Invoking to test cache files and get dictionary caches for the following movies:
movies_list = ["The Wizard of Oz", "King Kong", "Star Wars: Episode VI - Return of the Jedi"]
wizard_oz = get_movie_cache("The Wizard of Oz")
kingkong = get_movie_cache("King Kong")
return_jedi = get_movie_cache("Star Wars: Episode VI - Return of the Jedi")

# Accumulating those above dictionaries into one list
movie_cache_list = []
movie_cache_list.append(wizard_oz)
movie_cache_list.append(kingkong)
movie_cache_list.append(return_jedi)


# Class Setup
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

	def star_actor_tweets(self, searchterm):
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

class TwitterUser():
	def __init__(self, tweet_dict={}):
		self.screen_name = tweet_dict[0]['user']['screen_name']
		self.id = tweet_dict[0]['user']['id']
		self.favourites_count = tweet_dict[0]['user']['favourites_count']
		
	

class Tweet():
	def __init__(self, tweet_dict={}):
		self.text = tweet_dict['statuses'][0]['text']
		self.tweet_id = tweet_dict['statuses'][0]['id']
		self.screen_name = tweet_dict['statuses'][0]['user']['screen_name']
		self.movie_search = tweet_dict['search_metadata']['query'].replace("+"," ")
		self.num_favs = tweet_dict['statuses'][0]['favorite_count']
		self.retweets = tweet_dict['statuses'][0]['retweet_count']



# Creating a list of instances of class Movie using movie_cache_list
for movie in movie_cache_list:
	kong_class = Movie(movie_cache_list[0])
	jedi_class = Movie(movie_cache_list[1])
	wizard_class = Movie(movie_cache_list[2])

# Creating a new list of Movie class instances
movie_class_list = []
movie_class_list.append(kong_class)
movie_class_list.append(jedi_class)
movie_class_list.append(wizard_class)


# Invocations to Twitter functions to search for movie's top actor

kong_actor = kong_class.actors[0]
kong_top_actor = kong_class.star_actor_tweets(kong_actor)

jedi_actor = jedi_class.actors[0]
jedi_top_actor = jedi_class.star_actor_tweets(jedi_actor)

wizard_actor = wizard_class.actors[0]
wizard_top_actor = wizard_class.star_actor_tweets(wizard_actor)


# Accumulating all Tweet dictionaries into one list 
star_cache_list = []
star_cache_list.append(kong_top_actor)
star_cache_list.append(jedi_top_actor)
star_cache_list.append(wizard_top_actor)

# Creating a list of instances of class Tweet using star_cache_list
for star in star_cache_list:
	kong_star = Tweet(star_cache_list[0])
	jedi_star = Tweet(star_cache_list[1])
	wizard_star = Tweet(star_cache_list[2])

# Creating a new list of Tweet class instances
star_class_list = []
star_class_list.append(kong_star)
star_class_list.append(jedi_star)
star_class_list.append(wizard_star)

# Finding all users who posted and were mentioned in tweets
def get_twitter_users(string_of_users):
	pattern = r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9_]+)'
	result = re.findall(pattern, string_of_users)
	return result

user_list = []
user_list.append(kong_star.screen_name)
user_list.append(jedi_star.screen_name)
user_list.append(wizard_star.screen_name)
for i in get_twitter_users(kong_star.text):
	if i != []:
		user_list.append(i)

for k in get_twitter_users(jedi_star.text):
	if k != []:
		user_list.append(k)

for l in get_twitter_users(wizard_star.text):
	if l != []:
		user_list.append(l)

#Creating a list of instances of class TwitterUser using user_list
user_instances_list = []
for user in user_list:
	user_instances_list.append(get_twitter_cache(user))

user_class_list = []
for user_instance in user_instances_list:
	user_class_list.append(TwitterUser(user_instance))


#Database file setup
conn = sqlite3.connect('206_finalproject.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('DROP TABLE IF EXISTS Movies')
cur.execute('CREATE TABLE Tweets (tweet_id TEXT PRIMARY KEY, text TEXT, screen_name TEXT, movie_search TEXT, num_favs INTEGER, retweets INTEGER, FOREIGN KEY (screen_name) REFERENCES Users(screen_name), FOREIGN KEY (movie_search) REFERENCES Movies(top_actor))')
cur.execute('CREATE TABLE Users (user_id TEXT PRIMARY KEY, screen_name TEXT, num_favs INTEGER)')
cur.execute('CREATE TABLE Movies (movie_id TEXT PRIMARY KEY, movie_title TEXT, director TEXT, num_languages INTEGER, imdb_rating INTEGER, top_actor TEXT)')

#Adding all user data to Users table
for user in user_class_list:
	cur.execute("INSERT INTO Users (user_id, screen_name, num_favs) VALUES (?, ?, ?)", (user.id, user.screen_name, user.favourites_count))
conn.commit()

#Adding all movie data to Movies table
for movie in movie_class_list:
	cur.execute("INSERT INTO Movies (movie_id, movie_title, director, num_languages, imdb_rating, top_actor) VALUES (?, ?, ?, ?, ?, ?)", (movie.imdbID, movie.title, movie.director, movie.language, movie.imdb_rating, movie.actors[0]))
conn.commit()

#Adding all tweet data to Tweets table:
for tweet in star_class_list:
	cur.execute("INSERT INTO Tweets (tweet_id, text, screen_name, movie_search, num_favs, retweets) VALUES (?, ?, ?, ?, ?, ?)", (tweet.tweet_id, tweet.text, tweet.screen_name, tweet.movie_search, tweet.num_favs, tweet.retweets))
conn.commit()


#QUERIES

# The first query selects tweets and screen names where screen names are equal for the Tweets and Users tables, and pairs them together in a tuple.
query1 = 'SELECT Tweets.text, Tweets.screen_name FROM Tweets INNER JOIN Users ON Tweets.screen_name = Users.screen_name'
query1_result = []
for tup in cur.execute(query1):
	query1_result.append(tup)


# The second query selects all users' screen names and total number of favorites from the Users table only if that user has over 100 favorites.
# The data is then sorted by most popular user first with least popular last
query2 = 'SELECT Users.screen_name, Users.num_favs FROM Users WHERE num_favs > 100'
query2_result = []
for pop in cur.execute(query2):
	query2_result.append(pop)
ordered_users = sorted(query2_result, key = lambda x: x[1], reverse = True)


# The third query combines all the movies, the screennames of the individual who posted the tweet, and the top actor in the movie that they reference in their Tweet.
query3 = 'SELECT Movies.movie_title, Tweets.screen_name, Tweets.movie_search FROM Movies INNER JOIN Tweets ON Movies.top_actor = Tweets.movie_search'
query3_result = []
for t in cur.execute(query3):
	query3_result.append(t)


# Using datetime module to always have currently date in a variable for output purposes
now = datetime.datetime.now()
datepattern = now.strftime("%Y-%m-%d")

# Counter setup to find most common words in all tweets
c = Counter()
for tupz in query1_result:
	for word in tupz[0].split(" "):
		c[word] += 1
common_words = c.most_common(1)


# OUTPUTTING TO TEXT FILE
with open("SummaryStats.txt", "w") as infile:
	print("Summary Stats for: The Wizard of Oz, King Kong, and Star Wars: Episode VI - Return of the Jedi on {}".format(datepattern), file=infile)
	print("\n", file=infile)
	print("Popular Users: ", file=infile)
	for user in ordered_users:
		print("+{}".format(user[0]), file=infile), print("Total Favs: {}".format(user[1]), file=infile), print("\n", file=infile)
	for tup1 in query3_result:
		print("{} tweeted about {} from the movie {}".format(tup1[1], tup1[2], tup1[0]), file=infile)
	print("The most common word used was '{}' at '{}' uses".format(common_words[0][0], common_words[0][1]), file=infile)
	print("\n", file=infile)
	print("Full Tweets: ", file=infile)
	for tup2 in query1_result:
		print("+{}: {}".format(tup2[1], tup2[0]), file=infile)
infile.close()

# Tests are below.
class Task1(unittest.TestCase):
	def test_twitter_cache(self):
		f = open("SI206_finalproject_twittercache.json", "r")
		s = f.read()
		f.close()
		self.assertEqual(type(s),type(""), "Caching is not working correctly for twitter")
	def test_OMBD_cache(self):
		f = open("SI206_finalproject_OMDBcache.json", "r")
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
	def test_get_twitter_users(self):
		example = "Breaking: Michigan’s Jabrill Peppers tested positive for a diluted sample at the NFL scouting combine. (via @AdamSchefter)"
		result = get_twitter_users(example)
		self.assertTrue("AdamSchefter" in result, "Testing that regex pattern works correctly to extract Twitter user from tweet")
	def test_star_actor_tweets(self):
		wizard_class = Movie(wizard_oz)
		wizard_actor = wizard_class.actors[0]
		wizard_top_actor = wizard_class.star_actor_tweets(wizard_actor)
		self.assertEqual(type(wizard_top_actor), type({}), "Testing that the return type of star_actor_tweets class function is a dictionary")



if __name__ == "__main__":
	unittest.main(verbosity=2)