#news.py
from secrets import *
import requests
import json
from datetime import datetime

now = datetime.now()
sec_since_epoch = now.timestamp()
MAX_STALENESS = 30

CACHE_FNAME = 'cache_file_name.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)


def is_fresh(cache_entry):
    now = datetime.now().timestamp()
    staleness = now - cache_entry['cache_timestamp']
    return staleness < MAX_STALENESS

def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION:
        if is_fresh(CACHE_DICTION[unique_ident]):
            print("Getting cached data...")
            return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        resp = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        CACHE_DICTION[unique_ident]['cache_timestamp'] = datetime.now().timestamp()
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

# gets headlines for today's news
def fetch_top_headlines(category=None):
    baseurl = 'https://newsapi.org/v2/top-headlines'
    params={'country': 'us'}
    if category is not None:
        params['category'] = category
    params['apiKey'] = newsapi_key
    return make_request_using_cache(baseurl, params)

def get_headlines(results_dict):
    results = results_dict['articles']
    headlines = []
    for r in results:
        headlines.append(r['title'])
    return headlines

science_list_json = fetch_top_headlines('science')
headlines = get_headlines(science_list_json)
for h in headlines:
    print(h)
