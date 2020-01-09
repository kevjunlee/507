The data sources that I used in my project was the Last.FM web api. Their database can filter through many things like top artists, top tags, top tracks, but the specific thing that I wanted to focus on was geographic searches by country for top artists. In order to run the program, I have a pretty good help list in the interactive prompt that allows users to see what kind of inputs the code will accept. However, if ISO 3166-1 names are not used for my project, the json will return error API calls and the whole database and cache file will have to be thrown away. If the correct input is used, then there should be no problems. I also have a function in the user interface that will open a link to a reference page for ISO 3166-1 names for countries. 

My code is structured with a caching function, a request function, a table creation function, a function that populates the empty table with the json file that we received from the request function, and two functions that grab data from the data base and create graphs based on it. I also have comments in my code that explain what each function does for more clarity. The most important functions is compare_countries(), get_top_country_artists(), populate_json(), make_artist_table(), and country_bar_plot().

When you run the program using python3 final.py, it will prompt you to enter a command (or use help for options). If you type help into the command line, a help menu will pop up prompting users for four commands. It gives a description of what each command does and the parameters it accepts. Two of the functions even give examples of acceptable command inputs a user can use. The command topartists <Country> will return the top 10 artists for whatever country is selected and create a bar graph of that data. Top5pi will take in 5 country names and return the top 5 most frequently listened to artists amongst the five countries and show a pi chart of that data. The function list will send users to a reference page for acceptable parameters for the previous two functions by opening up a wikipedia link on the names for countries using the ISO 3166-1 format. The last command is exit which will exit the program
# final-project