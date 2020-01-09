import requests
import json
import secret
import plotly
import plotly.graph_objs as go


CLIENT_ID = secret.client_id
CLIENT_SECRET = secret.client_secret
MAPBOX_TOKEN = secret.MAPBOX_TOKEN
v = '20191101'

CACHE_FNAME = 'hw8.json'
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

def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl, params)
    if unique_ident in CACHE_DICTION:
        print('getting cached data...')
        return CACHE_DICTION[unique_ident]
    else:
        resp = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION, indent = 4)
        fw = open(CACHE_FNAME,'w')
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]
        
def get_foursquare(city, type):
    baseurl = 'https://api.foursquare.com/v2/venues/search?'
    params_dict = {}
    params_dict['client_id'] = CLIENT_ID
    params_dict['client_secret'] = CLIENT_SECRET
    params_dict['v'] = v
    params_dict['near'] = city
    params_dict['limit'] = 2
    params_dict['query'] = type
    response = requests.get(baseurl, params_dict)
    fdata = response.json()
    global finaldata
    finaldata = fdata['response']['venues']
    global ids
    ids = []
    for x in finaldata:
        ids.append(x['id'])
    return make_request_using_cache(baseurl, params_dict)

def get_pics_url(x):
    beginning = ''
    ending = ''
    size = '300X500'
    baseurl = 'https://api.foursquare.com/v2/venues/' + x + '/photos'
    params_dict = {}
    params_dict['limit'] = 1
    params_dict['client_secret'] = CLIENT_SECRET
    params_dict['client_id'] = CLIENT_ID
    params_dict['v'] = v
    response = requests.get(baseurl, params_dict)
    global fdata
    fdata = response.json()
    try:
        beginning = str(fdata['response']['photos']['items'][0]['prefix'])
        ending = str(fdata['response']['photos']['items'][0]['suffix'])
        complete_url = beginning + size + ending
        url_list.append(complete_url)
    except IndexError:
        url_list.append("No URL given")
        
        
# ----------------------------------------------
# Part 1: Get photo information using Flickr API
# ----------------------------------------------
print("----------------Part1--------------------")

city = input('In what city do you want to search: ')
type = input('What kind of place are you looking for: ')
type = type.lower()

get_foursquare(city, type)
url_list = []

for x in finaldata:
    print('Venue: ' + str(x['name']))
    print('Address: ' + str(x['location']['formattedAddress'][0]) + ', ' + str(x['location']['formattedAddress'][1]))
    print('Photo ID: ' + str(x['id']))
    print('\n')

# ----------------------------------------------
# Part 2: Map data onto Plotly
# ----------------------------------------------
for x in ids:
    get_pics_url(x)

lat_vals = []
lon_vals = []
text_vals = []
hover_vals = []

z = 0

for x in finaldata:
    lat_vals.append(finaldata[z]['location']['lat'])
    lon_vals.append(finaldata[z]['location']['lng'])
    text_vals.append(finaldata[z]['name'])
    z += 1
    
i = 0

for x in text_vals:
    hover_vals.append(x + '<br>' + url_list[i])
    i += 1

min_lat = float(min(lat_vals))
max_lat = float(max(lat_vals))
min_lon = float(min(lon_vals))
max_lon = float(max(lon_vals))

lat_axis = [min_lat -1, max_lat + 1]
lon_axis = [max_lon + 1, min_lon -1]

center_lat = (min_lat + max_lat) / 2
center_lon = (min_lon + max_lon) / 2

trace2 = dict(
    type = 'scattermapbox',
    lon = lon_vals,
    lat = lat_vals,
    text = hover_vals,
    hoverinfo = 'text',
    mode = 'markers',
    marker = dict(
        size = 8,
        symbol = 'circle',
        color = 'blue'
    ))

data = [trace2]

fig = go.Figure(data=data)
layout = dict(
    title = 'Venue Locations',
    autosize=True,
    showlegend = False,
    mapbox=dict(
        accesstoken=MAPBOX_TOKEN,
        bearing=0,
        center=dict(
            lat=38,
            lon=-94
        ),
        pitch=0,
        zoom=3,
      ),
)

fig = go.Figure(data=go.Scattermapbox(
    lon = lon_vals,
    lat = lat_vals,
    text = text_vals,
    mode = 'markers',
    marker_color = 'red',
    ))

fig.update_layout(layout)
fig.show()

