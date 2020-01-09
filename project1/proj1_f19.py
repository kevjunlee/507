import requests
import math
import json
import time
import webbrowser

def get_API_stuff(x = "", y = ""):
    baseurl = "https://itunes.apple.com/search?"
    params_dict = {}
    params_dict["term"] = x
    params_dict["limit"] = y
    response = requests.get(baseurl, params_dict)
    result = response.json()
    return result['results']

class Media:

    def __init__(self, title="No Title", author="No Author", releaseyear = "No Year", jsonDict = None):
        if jsonDict is None:
            self.title = title
            self.author = author
            self.releaseyear = releaseyear   
        else:
            self.process_json_dict(jsonDict)

    def process_json_dict(self, jsonDict):
        if 'trackName' in jsonDict.keys():
            self.title = jsonDict['trackName']
        else:
            self.title = jsonDict['collectionName']
        self.author = jsonDict['artistName']
        self.releaseyear = jsonDict['releaseDate'][0:4]
    
    def __str__(self):
        state = self.title + " by " + self.author + " (" + self.releaseyear + ")"
        return state
        
    def __len__(self):
        return 0
    

## Other classes, functions, etc. should go here
class Song(Media):
    
    def __init__(self, title="No Title", author="No Author", releaseyear = "No Year", album = "No Album", genre = "No Genre", tracklength = "No Length", jsonDict = None):
        super().__init__(title, author, releaseyear, jsonDict)
        if jsonDict is None:
            self.album = album
            self.genre = genre
            self.tracklength = tracklength
        else:
            self.process_json_dict(jsonDict)
    
    def process_json_dict(self, jsonDict):
        super().process_json_dict(jsonDict)
        self.album = jsonDict['collectionName']
        self.genre = jsonDict['primaryGenreName']
        self.tracklength = jsonDict['trackTimeMillis']
    
    def __str__(self):
        return super().__str__() + " [" + self.genre + "]"
    
    def __len__(self):
        return math.ceil(float(self.tracklength)/60)

class Movie(Media):
    
    def __init__(self, title="No Title", author="No Author", releaseyear = "No Year", rating = "No Rating", movielength = "No Length", jsonDict = None):
        super().__init__(title, author, releaseyear, jsonDict)
        if jsonDict is None:
            self.rating = rating
            self.movielength = movielength
        else:
            self.process_json_dict(jsonDict)
    
    def process_json_dict(self, jsonDict):
        super().process_json_dict(jsonDict)
        self.rating = jsonDict['contentAdvisoryRating']
        self.movielength = jsonDict['trackTimeMillis']
    
    def __str__(self):
        return super().__str__() + " [" + self.rating + "]"
    
    def __len__(self):
        return math.ceil(float(self.movielength)/3600)

def get_media_type(data):
    api_data = get_API_stuff(data)
    final_list = []
    songs = []
    movies = []
    medias = []
    for i in api_data:
        if i['wrapperType'] == 'track':
            if i['kind'] == 'song':
                songs.append(i)
            if i['kind'] == 'feature-movie':
                movies.append(i)
        else:
            medias.append(i)
    final_list = songs + movies + medias
    return final_list

    
if __name__ == "__main__":

    # your control code for Part 4 (interactive search) should go here
    choice = input("Enter a search term, or “exit” to quit: ")
    n = 1
    while choice != 'exit':
        api_search = get_media_type(choice)
        choice2 = int(input("Launch Preview (number of previews you'd like to see): "))
        print("\nSONGS")
        for song_entry in api_search:
            if choice2 == 0:
                break
            if song_entry['wrapperType'] == 'track':
                if song_entry['kind'] == 'song':
                    sing = Song(jsonDict=song_entry)
                    print(str(n) + " " + str(sing))
                    n += 1
                    choice2 -= 1
        print("\nMOVIES")
        for movie_entry in api_search:
            if choice2 == 0:
                break
            if movie_entry['wrapperType'] == 'track':
                if movie_entry['kind'] == 'feature-movie':
                    move = Movie(jsonDict=movie_entry)
                    print(str(n) + " " + str(move))
                    n += 1
                    choice2 -= 1
        print("\nMEDIA")
        for media_entry in api_search:
            if choice2 == 0:
                break
            if media_entry['wrapperType'] != 'track':
                med = Media(jsonDict=media_entry)
                print(str(n) + " " + str(med))
                n += 1
                choice2 -= 1
        choice = input("Enter a number for more info, another search term, or “exit” to quit: ")
        if choice.isdigit():
            choice = int(choice)
            print("\n")
            number = choice
            if 'trackViewUrl' in api_search[number - 1]:
                print("Launching " + str(api_search[number - 1]['trackViewUrl']) + " for you to learn some more! ")
                time.sleep(1.5)
                webbrowser.open(api_search[number - 1]['trackViewUrl'], new = 2)
            else:
                print("Unable to get more info, sorry")
            n = 1
            choice = input("Enter a number for more info, another search term, or “exit” to quit: ")
        n = 1
                
        
        
            


        


    


    
