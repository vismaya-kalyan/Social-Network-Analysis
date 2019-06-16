"""
Collect data.
"""

import tweepy 
import csv
from TwitterAPI import TwitterAPI
import sys
import time
import json

#Add your key and Secret of Twitter API here!!
consumer_key = '**************************'
consumer_secret = '*******************************************'
access_key = '*******************************'
access_secret = '************************************'
 
def collect_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets 
	#authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

	#initialize a list to hold all the tweepy Tweets
    alltweets = []	
	#make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200, include_rts=False)
	#save most recent tweets
    alltweets.extend(new_tweets)
	#save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    print ("   %s tweets downloaded" % (len(alltweets)))

	#keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:	
		#all subsiquent requests use the max_id param to prevent duplicates
    	new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest, include_rts=False)
		#save most recent tweets
    	alltweets.extend(new_tweets)
		#update the id of the oldest tweet less one
    	oldest = alltweets[-1].id - 1
    	print ("   %s tweets downloaded" % (len(alltweets)))

	#transform the tweepy tweets into a 2D array that will populate the csv	
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("ascii","ignore")] for tweet in alltweets]

	#write the csv	
    with open('%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)

    return len(alltweets)


# This method is done for you.
def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    return TwitterAPI(consumer_key, consumer_secret, access_key, access_secret)


# I've provided the method below to handle Twitter's rate limiting.
# You should call this method whenever you need to access the Twitter API.
def robust_request(twitter, resource, params, max_tries=5):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request; e.g., "friends/ids"
      params ..... A parameter dict for the request, e.g., to specify
                   parameters like screen_name or count.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print("Got error %s \nsleeping for 15 minutes." % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)


def get_users(twitter, screen_names):
    """Retrieve the Twitter user objects for each screen_name.
    Params:
        twitter........The TwitterAPI object.
        screen_names...A list of strings, one per screen_name
    Returns:
        A list of dicts, one per user, containing all the user information
        (e.g., screen_name, id, location, etc)

    See the API documentation here: https://dev.twitter.com/rest/reference/get/users/lookup
    """
    params = {"screen_name": screen_names}
    return robust_request(twitter, "users/lookup", params)


def get_tweets(twitter, search, name):
    
    tweets = list()
    temp = list()

    # Fetching data
    for tweet in robust_request(twitter, 'search/tweets', search):
        if 'free' not in tweet['text'].lower() and 'giveaway' not in tweet['text'].lower() and 'win' not in tweet['text'].lower():
            temp.append(tweet)
    tweets.extend(temp)

    # Selecting minimum ID of tweets obtained
    min_id = temp[0]['id']
    for i in range(len(temp)):
        if min_id > temp[i]['id']:
            min_id = temp[i]['id']

    # Fetching more data
    for _ in range(12):
        temp = list()
        search['max_id'] = min_id-1
        for tweet in robust_request(twitter, 'search/tweets', search):
            if 'free' not in tweet['text'].lower() and 'giveaway' not in tweet['text'].lower() and 'win' not in tweet['text'].lower():
                temp.append(tweet)
        tweets.extend(temp)
        min_id = temp[0]['id']
        for i in range(len(temp)):
            if min_id > temp[i]['id']:
                min_id = temp[i]['id']

    # writing data to JSON file
    data = open('%s_tweets.json'%name, 'w')
    json.dump(tweets, data)
    data.close()


def main():

    summary = open('collect.txt', 'w')  # Create file to write summary
    screen_names = ['jordanbpeterson','joerogan']
    twitter = get_twitter()
    users = sorted(get_users(twitter, screen_names), key=lambda x: x["screen_name"])
  
    count = []
    for i in screen_names:
        print(i)
        count.append(collect_tweets(i))

    summary.write('Number of users collected: ' + str(len(screen_names)) + '\n')
    summary.write('jordanbpeterson \n')
    summary.write('joerogan \n\n')
    summary.write('Number of tweets fetched by jordanbpeterson ' + str(count[0]))
    summary.write('\nNumber of tweets fetched by joerogan ' + str(count[1]))
    
    print('\nNumber of users collected: ' + str(len(screen_names)) + '\n')
    print('jordanbpeterson \n')
    print('joerogan \n\n')
    print('Number of tweets fetched by jordanbpeterson ' + str(count[0]))
    print('\nNumber of tweets fetched by joerogan ' + str(count[1]))


    # Get tweets which contain jordanbpeterson and joerogan
    get_tweets(twitter, {'q': 'jordanbpeterson', 'count': 100, 'lang': 'en'},'jordanbpeterson') 
    get_tweets(twitter, {'q': 'joerogan', 'count': 100, 'lang': 'en'},'joerogan') 

    summary.write('\nNumber of tweets collected including jordanbpeterson in them 100')
    summary.write('\nNumber of tweets collected including joerogan in them 100')

    print('\nNumber of tweets collected including jordanbpeterson in them 100')
    print('\nNumber of tweets collected including joerogan in them 100')

    summary.close() 

if __name__ == "__main__":
    main()

