from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
# Uncomment following two lines after you install nltk
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

## SI 507 - HW5
## COMMENT WITH:
## Your section day/time: Lecture - Tuesday 8:30-11:30 AM  / Discussion - Wednesday 10-11:30 AM
## Any names of people you worked with on this assignment: Iain Graham

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching

CACHE_FNAME = 'cache_file_name.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)
    
#Code for Part 1:Get Tweets

def get_tweets(username, num_tweets):
    baseurl = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=umsi&count=25'
    params_dict = {}
    params_dict["screen_name"] = username
    params_dict["count"] = num_tweets
    unique_combo = params_unique_combination(baseurl, params_dict)
    if unique_combo in CACHE_DICTION:
        print("Getting cached data...")
        return(CACHE_DICTION[unique_combo])
    else:
        print("Making a request for new data...")
        response = requests.get(baseurl, params_dict, auth=auth)
        twdata = json.loads(response.text)
        twitDict = {}
        twitDict['statuses'] = twdata
        CACHE_DICTION[unique_combo] = twitDict
        cache_file = open(CACHE_FNAME, "w")
        cached_data = json.dumps(CACHE_DICTION, indent = 2)
        cache_file.write(cached_data)
        cache_file.close()
        return CACHE_DICTION[unique_combo]

twitDict = get_tweets(username, num_tweets)
twitterDict = "tweet.json"
t = open(twitterDict, 'w')
twitterJson = json.dumps(twitDict, indent = 4)
t.write(twitterJson)
t.close()

get_tweets(username, num_tweets)

#Code for Part 2:Analyze Tweets
stop_words = set(stopwords.words('english'))
WORD_RE = re.compile(r"\w+")
token_list = []
for x in twitDict['statuses']:
    token = nltk.word_tokenize(x['text'])
    for y in token:
        if y.lower() not in stop_words:
            token_list.append(y)
filtered_list = list(filter(WORD_RE.match, token_list))
for x in filtered_list:
    if "RT" in filtered_list: filtered_list.remove("RT")
    if "http" in filtered_list: filtered_list.remove("http")
    if "https" in filtered_list: filtered_list.remove("https")
distribution = nltk.FreqDist(filtered_list)
sorted_distribution = sorted(distribution.items(), key = lambda x: x[1], reverse = True)
print("5 most frequently used words (word, frequency): ")
for x in sorted_distribution[0:5]:
    print(x)

if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()

    
