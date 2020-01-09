# 507 Homework 6 Part 1
import requests
from bs4 import BeautifulSoup

#### Part 1 ####
print('\n*********** PART 1 ***********')
print("-------Alt tags-------\n")

### Your Part 1 solution goes here

html = requests.get('http://newmantaylor.com/gallery.html').text

soup = BeautifulSoup(html, 'html.parser')

images = soup.find_all('img')


for picture in images:
    try: print(picture['alt'])
    except: print('No alternative text provided!')
    
