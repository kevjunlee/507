## proj_nps.py
## Skeleton for Project 2 for SI 507
## ~~~ modify this file, but don't rename it ~~~
from secrets import google_places_key
from secrets import MAPBOX_TOKEN
import requests
from bs4 import BeautifulSoup
import json
import plotly.graph_objs as go
import plotly


CACHE_FNAME = 'project2.json'
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

def make_second_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl, params)
    if unique_ident in CACHE_DICTION:
        print('getting cached data...')
        return CACHE_DICTION[unique_ident]
    else:
        resp = requests.get(baseurl, params)
        data = json.loads(resp.text)
        CACHE_DICTION[unique_ident] = data
        dumped_json_cache = json.dumps(CACHE_DICTION, indent = 4)
        fw = open(CACHE_FNAME,'w')
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NationalSite():
    def __init__(self, type, name, desc, url = None, street = None, city = None, state = None, zipcode = None):
        self.type = type
        self.name = name
        self.description = desc
        self.url = url
        
        if url != None:
            park_info = requests.get(url).text
            park_info_soup = BeautifulSoup(park_info, 'html.parser')
            try:
                self.address_street = park_info_soup.find('span', itemprop = 'streetAddress').text.split('\n')[1]
            except:
                self.address_street = 'Street address info unavailable'
            try:
                self.address_city = park_info_soup.find('span', itemprop = 'addressLocality').text
            except:
                self.address_city = 'City info unavailable'
            try:
                self.address_state = park_info_soup.find('span', itemprop = 'addressRegion').text
            except:
                self.address_state = 'State info unavailable'
            try:
                self.address_zip = park_info_soup.find('span', itemprop = 'postalCode').text[:-5]
            except:
                self.address_zip = 'Postal code info unavailable'

    
    def __str__(self):
        return self.name + " (" + self.type + "): " + self.address_street + ", " + self.address_city + ", " + self.address_state + " " + self.address_zip

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NearbyPlace():
    def __init__(self, name, lat = 0, lon = 0):
        self.name = name
        self.lat = lat
        self.lon = lon
    
    def __str__(self):
        return self.name

## Must return the list of NationalSites for the specified state
## param: the 2-letter state abbreviation, lowercase
##        (OK to make it work for uppercase too)
## returns: list of all of the NationalSites
##        (e.g., National Parks, National Heritage Sites, etc.) that are listed
##        for the state at nps.gov
def get_sites_for_state(state_abbr):
    sites_list = []
    baseurl = 'https://www.nps.gov/state/'
    state_url = baseurl + state_abbr.lower() + '/index.htm'
    state_scrape = requests.get(state_url).text
    state_soup = BeautifulSoup(state_scrape, 'html.parser')
    parks_list = state_soup.find_all('li', class_ = 'clearfix')

    for x in parks_list[:-1]:
        name = x.find('a').text
        try:
            park_type = x.find('h2').text.strip()
        except:
            park_type = 'No park type'
        desc = x.find('p').text[1:-1]
        urls_park = 'https://www.nps.gov' + x.find('a')['href'] + 'planyourvisit/basicinfo.htm'
        park = NationalSite(park_type, name, desc, urls_park)
        sites_list.append(park)
    return sites_list

## Must return the list of NearbyPlaces for the specific NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list
def get_nearby_places_for_site(national_site):
    coordinate_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
    nearby_places = []
    params = {}
    params['key'] = google_places_key
    params['input'] = national_site.name + ' ' + national_site.type
    params['inputtype'] = 'textquery'
    params['fields'] = 'geometry'
    
    first_search = make_second_request_using_cache(coordinate_url, params)
    results = first_search['candidates'][0]
    try:
        lat_of_place = results['geometry']['location']['lat']
        lon_of_place = results['geometry']['location']['lng']
    except:
        return None
    coordinates_of_place = str(lat_of_place) + ',' + str(lon_of_place)
#    print(coordinates_of_place)

    if coordinates_of_place == None:
        return []
    else:
        params2 = {}
        new_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(coordinates_of_place)
        params2['key'] = google_places_key
        params2['radius'] = '10000'
        second_search = make_second_request_using_cache(new_url, params2)
        results2 = second_search['results']
        for x in results2:
            name_of_place = x['name']
            lat_of_place = x['geometry']['location']['lat']
            lon_of_place = x['geometry']['location']['lng']
            place = NearbyPlace(name_of_place, lat_of_place, lon_of_place)
            nearby_places.append(place)
    return nearby_places

#site1 = NationalSite('National Monument',
#'Sunset Crater Volcano', 'A volcano in a crater.')
#get_nearby_places_for_site(site1)
## Must plot all of the NationalSites listed for the state on nps.gov
## Note that some NationalSites might actually be located outside the state.
## If any NationalSites are not found by the Google Places API they should
##  be ignored.
## param: the 2-letter state abbreviation
## returns: nothing
## what it needs to do: launches a page with a plotly map in the web browser
def plot_sites_for_state(state_abbr):
    lat_vals = []
    lon_vals = []
    text_vals = []
    sites_list = get_sites_for_state(state_abbr)
    new_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
    params3 = {}
    params3['key'] = google_places_key
    params3['fields'] = 'geometry'
    params3['inputtype'] = 'textquery'
    
    
    for site in sites_list:
        params3['input'] = site.name + ' ' + site.type
        site_data = make_second_request_using_cache(new_url, params3)
        if len(site_data['candidates']) != 0:
            site_lat = site_data['candidates'][0]['geometry']['location']['lat']
            site_lon = site_data['candidates'][0]['geometry']['location']['lng']
            lat_vals.append(site_lat)
            lon_vals.append(site_lon)
            text_vals.append(site.name)
    

    min_lat = float(min(lat_vals))
    max_lat = float(max(lat_vals))
    min_lon = float(min(lon_vals))
    max_lon = float(max(lon_vals))

    lat_axis = [min_lat, max_lat]
    lon_axis = [max_lon, min_lon]

    layout = dict(
        title = 'National Parks in ' + state_abbr.upper(),
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(100, 217, 217)",
            countrycolor = "rgb(217, 100, 217)",
            lataxis = {'range': lat_axis},
            lonaxis = {'range': lon_axis},
            countrywidth = 3,
            subunitwidth = 3
        ))

    fig = go.Figure(data=go.Scattergeo(
        lon = lon_vals,
        lat = lat_vals,
        text = text_vals,
        mode = 'markers',
        marker_color = 'red',
        ))

    fig.update_layout(layout)
    fig.show()


## Must plot up to 20 of the NearbyPlaces found using the Google Places API
## param: the NationalSite around which to search
## returns: nothing
## what it needs to do: launches a page with a plotly map in the web browser
def plot_nearby_for_site(site_object):
    site_lat_vals = []
    site_lon_vals = []
    site_text_vals = []
    lat_vals = []
    lon_vals = []
    text_vals = []

    params4 = {}
    params4['key'] = google_places_key
    params4['input'] = site_object.name + ' ' + site_object.type
    params4['inputtype'] = 'textquery'
    params4['fields'] = 'geometry'
    new_url2 = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
    site_info = make_second_request_using_cache(new_url2, params4)
    try:
        site_lat = site_info['candidates'][0]['geometry']['location']['lat']
        site_lon = site_info['candidates'][0]['geometry']['location']['lng']
    except:
        pass
        
    site_lat_vals.append(site_lat)
    site_lon_vals.append(site_lon)
    site_text_vals.append(site_object.name)
    nearby_places_list = get_nearby_places_for_site(site_object)
    
    for nearbysite in nearby_places_list:
        if nearbysite.name != site_object.name:
            lat_vals.append(nearbysite.lat)
            lon_vals.append(nearbysite.lon)
            text_vals.append(nearbysite.name)

    min_lat = float(min(lat_vals))
    max_lat = float(max(lat_vals))
    min_lon = float(min(lon_vals))
    max_lon = float(max(lon_vals))

    lat_axis = [min_lat -1, max_lat + 1]
    lon_axis = [max_lon + 1, min_lon -1]

    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    trace1 = dict(
        type = 'scattermapbox',
        # locationmode = 'USA-states',
        lon = site_lon_vals,
        lat = site_lat_vals,
        text = site_text_vals,
        hoverinfo = 'text',
        mode = 'markers',
        marker = dict(
            size = 19,
            symbol = 'star',
            color = 'blue'
        ))

    trace2 = dict(
        type = 'scattermapbox',
        lon = lon_vals,
        lat = lat_vals,
        text = text_vals,
        hoverinfo = 'text',
        mode = 'markers',
        marker = dict(
            size = 8,
            symbol = 'circle',
            color = 'red'
        ))
    
    data = [trace1, trace2]
    fig = go.Figure(data=data)
    
    layout = dict(
        title = 'Sites nearby ' + site_object.name,
        geo_scope='usa',
        autosize=True,
        showlegend = False,
        mapbox=dict(
            accesstoken=MAPBOX_TOKEN,
            bearing=0,
            center=dict(
                lat=center_lat,
                lon=center_lon
            ),
            pitch=0,
            zoom=9,
        )
    )
    fig.update_layout(layout)
    fig.write_html('plots_sites_for_states.html', auto_open = True)
    
if __name__ == '__main__':
    input1 = input('Welcome! Enter a command (or help for options): ')
    
    while input1 != 'exit':
        if input1 == 'help':
            print('Here is a list of commands you can use: ')
            print('   list <state_abbr>')
            print('       available anytime')
            print('       lists all National Sites in a state')
            print('       valid inputs: a two-letter state abbreviation')
            print('   nearby <result_number>')
            print('       available only if there is an active site list')
            print('       list all Places nearby a given result')
            print('       valid inputs: an integer 1-len(result_set_size)')
            print('   map <option>')
            print('       available only if there is an active site or nearby result list')
            print('       displays the current results on a map')
            print('   exit')
            print('       exits the program')
            print('   help')
            print('       lists all available commands (these instructions)')
        elif input1[:4] == 'list':
                state = input1[-2:]
                print('National Sites in ' + state.upper())
                sites = get_sites_for_state(state)
                i = 1
                for site in sites:
                    print(i, site)
                    i = i + 1
                print('Available commands for next step: ')
                print('   - nearby <result_number> to view places near one of the sites above')
                print('   - map sites to view the site list above on a map')
                print('   - list <state> to do a search for another state')
            
        elif input1[:6] == 'nearby':
            try:
                site_entered = int(input1[7:])-1
                print('Places near ' + sites[site_entered].name)
                places = get_nearby_places_for_site(sites[site_entered])
                i = 1
                for place in places:
                    print(i, place)
                    i = i + 1
                print('Now you can type: ')
                print('   - map nearby to view the nearby list above on a map')
                print('   - nearby <result_number> to view places near another site')
                print('   - map sites to view the last site list on a map')
                print('   - list <state> to do a search for another state')
            except:
                print('Error: You need a site list first. Try typing list <state>.')
            
        elif input1[:3] == 'map':
            if input1[4:] == 'sites':
                try:
                    plot_sites_for_state(state)
                except:
                    print('Error: Site list required. Try typing list <state>.')
            elif input1[4:] == 'nearby':
                try:
                    plot_nearby_for_site(sites[site_entered])
                except:
                    print('Error: Nearby list required. Try typing nearby <result_number> if site list is already given.')
            else:
                print('Error: Sorry, not a functional command. Please try again or enter help.')
            
        else:
            print('Error: Sorry, not a functional command. Please try again or enter help.')
                
        input1 = input('Enter a command (or help for options): ')

        print('Thanks for using this program. Goodbye!')

