SI 206 Final Project - Option 2
Written by Miguel Martinez

I picked option 2, the OMDB and Twitter Mashup option. 

What does it do? What can it be used for? Is there any input required? What is the output? Is a database created?

- This code will get and cache data from Twitter (from a specified searchterm and about a Twitter user) and get and cache data from the
OMDB API for three movie titles: The Wizard of Oz, King Kong, and Star Wars: Episode VI - Return of the Jedi. A .txt file called 'SummaryStats.txt' will be created
at the end of the program, representing a page detailing information such as Twitter users, who they tweeted about, etc. Additionally, three .json files will be created under the following names: 'SI206_finalproject_OMDB.json', 'SI206_finalproject_starcache.json', and 'SI206_finalproject_twittercache.json' - these will contain the cached contents. Lastly, a database file is created called '206_finalproject.db' which houses three tables: Movies, Tweets, and Users.

How do you run it? 

- To correctly run the file, one file is needed in the directory that the 206_finalproject.py file is in. A 'twitter_info.py' is required to be able to cache any content from Twitter. If that condiditon is fulfilled, then nothing more is needed to launch the file.

What are its dependencies? Any modules, or particular files needed?

- twitter_info.py (mentioned above)
- unittest module
- itertools module
- collections module
- tweepy module
- json module
- sqlite3 module
- re module
- Counter module
- sys module
- codecs module
- requests module
- datetime module

What files are included? 

- 206_finalproject.py (this is the main file to run)
- 206_finalproject.db (this is the database file for the code, not needed to run for first time)
- 206_finalproject_OMDBcache.json (cache file containing information about the three movies)
- 206_finalproject_starcache.json (cache file containing information about tweets discussing top actors in three movies)
- 206_finalproject_twittercache.json (cache file containing user information resulting from tweets)
- SummaryStats.txt (a text file containing summary information about the data collected)
- README.txt (this readme file, detailing the usage and specifications of the other files!)

Each Function listed with: name, input, return value, and behavior (if no return value)

- get_twitter_cache: requires a user's Twitter handle, will return a dictionary object representing that user's profile
- get_movie_cache: requires the name of a movie, will return a dictionary object representing that movie's information from the OMDB API
- get_twitter_users: requires a string of text (such as a Tweet), will use regex to find Twitter users, and will return a list of Twitter user handles, if they are in the body of text.

Each Class with: name, any input besides self, behavior, return value?

- Movie Class
-- Requires a dictionary object representing a movie
-- Initializes six instance variables: imdbID, title, director, imdb_rating, actors, and language
-- __str__ method: no input needed, will return a string representing basic facts of the movies
-- star_actor_tweets method: requires a searchterm as input (in this case, the name of a star actor/actress) and will return a dictionary object representing tweets that actor is mentioned in.
-- Returns Nothing

-TwitterUser Class
-- Requires a dictionary object representing a Twitter user
-- Initializes three instance variables: screen_name, id, favourites_count
-- Returns Nothing

-Tweet Class
-- Requires a dictionary object representing a Twitter user
-- Initializes six instance variables: text, tweet_id, screen_name, movie_search, num_favs, and retweets
-- Returns Nothing

Each table in the database: what does each row represent, what attributes are in each row?

- Movies Table
-- Each row represents a different movie (The Wizard of Oz, King Kong, Star Wars Episode VI - Return of the Jedi)
-- Attributes for each row: movie_id, movie_title, director, num_languages, imdb_rating, and top_actor

- Tweets Table
-- Each row represents a different tweet, one for each movie's top actor. 
-- Attributes for each row: tweet_id, text, screen_name, movie_search, num_favs, and retweets

- Users Table
-- Each row represents a different user that was mentioned in the tweet text, the "neighborhood"
-- Attributes for each row: user_id, screen_Name, and num_favs


For data manipulation (queries and text output): what does it do? how is it useful? what will it show you? What should a user expect?

- The first query selects tweets and screen names where screen names are equal for the Tweets and Users tables, and pairs them together in a tuple.
- The second query selects all users' screen names and total number of favorites from the Users table only if that user has over 100 favorites. The data is then sorted by most popular user first with least popular last.
- The third query combines all the movies, the screennames of the individual who posted the tweet, and the top actor in the movie that they reference in their Tweet.
- Datetime module is utilized to always output current date to output file
- Counter is utilized to find most common word used in tweets, and output that to the output file
- Output file, 'SummaryStats.txt' will output the following information: movies that were used along with the date of the data collection, the most popular users found within the neighborhood (screen name and total amount of favorites are listed), what actor/actress and movie each user tweeted about along with their screen name, and lastly, the actual text of the tweet is listed. 

Why did you choose to do this project?

- I wanted to choose this project because I wanted to work with two APIS, rather than work with one extensive API. Additionally, I was considering Option 3 and utilizing my own found APIs, but after a bit of struggling to come up with a decent combination, I decided to go with Option 2.


Line(s) on which each of your data gathering functions begin(s): 44, 69, 125
Line(s) on which your class definition(s) begin(s): 113, 140, 148
Line(s) where your database is created in the program: 235
Line(s) of code that load data into your database: 237-257
Line(s) of code (approx) where your data processing code occurs — where in the file can we see all the processing techniques you used?: 263-294
Line(s) of code that generate the output: 298-311

