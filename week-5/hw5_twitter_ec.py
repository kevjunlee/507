from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
# Uncomment following two lines after you install nltk
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import re

## SI 507 - HW5
## COMMENT WITH:
## Your section day/time: Section 001
## Any names of people you worked with on this assignment: Iain Graham

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]
username2 = sys.argv[3]
num_tweets2 = sys.argv[4]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth end

#Write your code below:
#Code for Part 1:Get Tweets

CACHE_FNAME = 'twitter_cache.json'
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
    return baseurl + "_" + "_".join(res)

def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl, params)

    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a new request...")
        resp = requests.get(baseurl, params, auth = auth)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

def get_tweets(username, num_tweets):
    baseurl = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params_dict = {}
    params_dict['screen_name'] = username
    params_dict['count'] = num_tweets
    return make_request_using_cache(baseurl, params_dict)

one = get_tweets(username, num_tweets)
two = get_tweets(username2, num_tweets2)

#Code for Part 2:Analyze Tweets

def list_of_tweets(tweets):
    words = []
    for word_dict in tweets:
        words.append(word_dict['text'])
    return words

tweet1 = list_of_tweets(one)
tweet2 = list_of_tweets(two)

twitlist1 = []
for x in tweet_list:
    token = nltk.word_tokenize(x)
    twitlist1.append(token)

twitlist2 = []
for x in tweet_list2:
    token = nltk.word_tokenize(x)
    twitlist2.append(token)

token_list = []
for lists in twitlist1:
    for words in lists:
        token_list.append(words)

token_list2 = []
for lists in twitlist2:
    for words in lists:
        token_list2.append(words)

dist = FreqDist(token_list)
dist2 = FreqDist(token_list2)

stop_words = set(stopwords.words('english'))
filtered_list = [w for w in token_list if not w in stop_words]
filtered_list2 = [w for w in token_list2 if not w in stop_words]

filtered_list = []
for w in token_list:
    if w not in stop_words:
        filtered_list.append(w)

filtered_list2 = []
for w in token_list2:
    if w not in stop_words:
        filtered_list2.append(w)

r = re.compile(r"\w+")
word_list = list(filter(r.match, filtered_list))
word_list2 = list(filter(r.match, filtered_list2))

for x in word_list:
    if 'RT'in word_list: word_list.remove('RT')
    if 'http'in word_list: word_list.remove('http')
    if 'https'in word_list: word_list.remove('https')

for x in word_list2:
    if 'RT'in word_list2: word_list2.remove('RT')
    if 'http'in word_list2: word_list2.remove('http')
    if 'https'in word_list2: word_list2.remove('https')

new = list(set(word_list) & set(word_list2))

print(len(word_list2))

common = []
for x in word_list:
    if x in new:
        common.append(x)

common2 = []
for x in word_list2:
    if x in new:
        common2.append(x)

in_common = common + common2

common_dist = FreqDist(in_common)
print("Top commonalities between the two accounts" + str(common_dist.most_common(5)))

for x in word_list:
    if x in new:
        word_list.remove(x)

common_first = FreqDist(word_list)
print(common_first.most_common(5))

for x in word_list2:
    if x in new:
        word_list2.remove(x)

common_second = FreqDist(word_list2)
print(common_second.most_common(5))

#Code for Part 3:Caching

if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
