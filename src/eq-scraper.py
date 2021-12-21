import requests
from bs4 import BeautifulSoup
import json
import re
import pathlib
import os

# Scraping Part
URL = 'http://www.koeri.boun.edu.tr/scripts/lst6.asp'
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')
text = str(soup.pre.string)
text = text[578:] # Filter redundant letters.
earthquakes = text.split('İlksel')

# Creating a dictionary and saving as a JSON file.
# API data function
def create_api_data(earthquakes):
    data_array = []
    for eq in earthquakes:
        # date, latitude, longitude, deep, md, ml, mw
        set_one = re.findall("([0-9]+(\\.[0-9]+)+)", eq.strip())
        # time
        set_two = re.findall("(([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?(:([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?)+)",
                    eq.strip())
        # place
        set_three = re.findall("[a-zA-Z]+", eq.strip())
        # Get the magnitude of the earthquake
        if(set_one):
            if (len(set_one) == 7):
                ml = set_one[5][0]
            elif (len(set_one) == 6):
                ml = set_one[4][0]
            else:
                ml = set_one[4][0]
            # Put all data together
            data_set = {
                "Date": set_one[0][0],
                "Time": set_two[0][0],
                "Latitude": set_one[1][0],
                "Longitude": set_one[2][0],
                "Depth": set_one[3][0],
                "ML": ml,
                "Location": ' '.join(set_three)
                
            }
            # Push data to the array
            data_array.append(data_set)
    return data_array

data_array = create_api_data(earthquakes)
api_data = {
    "data": data_array
}

# Save API data
repo_root_dir = pathlib.Path(__file__).resolve().parent.parent
repo_root_dir = pathlib.Path(os.path.relpath(repo_root_dir))
with open(repo_root_dir / 'api-data/api_data.json', 'w', encoding='utf-8') as f:
    json.dump(api_data, f, indent=4)



