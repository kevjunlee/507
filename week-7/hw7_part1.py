# 507 Homework 7 Part 1
import requests
import json
from bs4 import BeautifulSoup

global variable_header

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)
    
    if unique_ident in CACHE_DICTION:
        print("Getting cache data...")
        return CACHE_DICTION[unique_ident]
    else:
        variable_header = {'User-Agent': 'SI_CLASS'}
        resp = requests.get(url, headers=header)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

#### Your Part 1 solution goes here ####
def get_umsi_data(page):
    #### Implement your function here ####
    umsi_people = {}
    baseurl = 'https://www.si.umich.edu'
    directory_url = baseurl + '/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All&page=' + str(page)
    variable_header = {'User-Agent': 'SI_CLASS'}
    page_text = make_request_using_cache(directory_url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    views = page_soup.find_all(class_='views-row')

    for i in range(len(views)):
        name = views[i].find(class_='field-name-title').text
        title = views[i].find(class_='field-name-field-person-titles').text
        detailed_url = views[i].find(class_='field-name-contact-details').find('a')['href']
        detail_url = baseurl + detailed_url
        page_elements = make_request_using_cache(detail_url)
        page_elements_soup = BeautifulSoup(page_elements, 'html.parser')
        email = page_elements_soup.find(class_='field-name-field-person-email').find(class_='field-items').text
        umsi_people[email] = {"name": name , "title": title }

    return umsi_people

#### Execute funciton, get_umsi_data, here ####
umsi_stuff = {}
for i in range(14):
    umsi_stuff.update(get_umsi_data(i))

print(umsi_stuff)

#### Write out file here #####
dumped_directory = json.dumps(umsi_stuff, indent=2)
fw = open('directory_dict.json', 'w')
fw.write(dumped_directory)
fw.close()
