## Your name: Miguel Martinez
## The option you've chosen: OPTION 2

# Put import statements you expect to need here!
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
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)


# Write your test cases here.
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
	def test_
## Remember to invoke all your tests...
if __name__ == "__main__":
	unittest.main(verbosity=2)