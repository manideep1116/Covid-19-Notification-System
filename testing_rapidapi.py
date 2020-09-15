import requests
import json

total_url = "https://services2.arcgis.com/w657bnjzrjguNyOy/arcgis/rest/services/covid19_by_zip_expanded_1/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"
#url = "https://opendata.arcgis.com/datasets/5a10c212d4cf4cbd95de7207f0805730_0.geojson"
url = "https://opendata.arcgis.com/datasets/7ad849e453684ea09f92ac56bd97a08e_0.geojson"
# headers = {
#     'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com",
#     'x-rapidapi-key': "4fe7a8dc75msh832cee3bef8a575p1d2c45jsn9f05873d3f4d"
#     }

def cases_zip(zip_url):
    with requests.get(zip_url) as r_zip:
        cases = json.loads(r_zip.text)
        for i in range(len(cases['features'])):
            if cases['features'][i]['attributes']['zip_5'] ==63146:
                #f.write('The number of total cases in the zip code 63146 are '+ "'"+ str(cases['features'][i]['properties']['cases'])+ "'"+" on " +str( time)+"\n"*2)
                #{'zip_5': 63025, 'cases_total': 291, 'cases_new': 50, 'cases_new_youth': 0, 'population': 8369, 'population_youth': 2589, 'cases_total_100k': 3477.1, 'cases_new_100k': 597.4, 'cases_new_youth_100k': '0', 'ObjectId': 1}
                return cases['features'][i]['attributes']['cases_new']
                print(cases['features'][i]['attributes']['cases_new'])
                break

response = requests.request("GET", total_url)

r = response.text
#print(response.text)
cases_zip(total_url)
