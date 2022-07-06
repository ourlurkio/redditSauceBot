from bs4 import BeautifulSoup
import requests
import json

#this file is used once to create a json of recipes from a given website. Script written specifically to work with
# url included in this file, but can easily be modified if different source of sauce wanted

url = "https://www.thespruceeats.com/simple-sauce-recipes-101780"

# set url to be scraped for sauce recipes
recipe_url = "https://www.thespruceeats.com/simple-sauce-recipes-101780"

# get page data, then parse the data
recipe_data_raw = requests.get(url=recipe_url).text
recipe_data_parsed = BeautifulSoup(recipe_data_raw, 'html.parser')

# create list to store each property as a dict. Dict keys as address, pcm and link
recipe_list = []

# loop through parsed data, and pull out each recipe. Find each item and enter as value to key at list pos
recipe_all = recipe_data_parsed.find_all('a', class_="mntl-sc-block-heading__link")

for recipe in recipe_all:
    temp_dict = {}
    temp_dict['name'] = recipe.text.strip('\n')
    temp_dict['link'] = recipe.get('href')
    recipe_list.append(temp_dict)

with open('recipe_json.json','w') as out_file:
    json.dump(recipe_list,out_file)
    out_file.close()



