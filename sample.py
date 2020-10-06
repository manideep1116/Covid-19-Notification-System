import requests
import json
import csv  
from datetime import datetime, date
import pandas as pd
import matplotlib.pyplot as plt

r_county = 'https://covid19-us-api.herokuapp.com/county'
r_zipcode = "https://services2.arcgis.com/w657bnjzrjguNyOy/arcgis/rest/services/covid19_by_zip_expanded_1/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"
# r_zipcode = 'https://opendata.arcgis.com/datasets/7ad849e453684ea09f92ac56bd97a08e_0.geojson'
#https://data-stlcogis.opendata.arcgis.com/datasets/covid-19-zip-code-data-w-past-14-days/geoservice?page=5&selectedAttribute=cases_new
#r_state =  'https://covidtracking.com/api/states'
r_state = 'https://covidtracking.com/api/states/daily'
now = datetime.now()
today = date.today()
time = today.strftime("%m/%d/%y")

# Setting threshold for number of cases in zip, state and county

# Danger zone
dangerzone_zip = 50
dangerzone_state = 1400
dangerzone_county = 200
# Cautious Zone
moderatezone_zip = 25
moderatezone_state = 700
moderatezone_county = 100
# Moderate Zone
safezone_zip = 5
safezone_state = 200
safezone_county = 20 
# Safe Zone

# def cases_MO(state_url,filename=''):
#   if filename:
#       pass
#   else:
#       filename = cases_MO.txt
#   with requests.get(state_url) as r_state:
#       with open(filename, 'a') as f:
#          cases=json.loads(r_state.text)
#          for i in range(len(cases)): 
#              if cases[i]['state']== 'MO': 
#                 MO_cases = cases[i]['positiveIncrease']
#                 f.write('The number of new cases in Missouri are '+ "'"+str(MO_cases)+"'"+" on " +str( time) +"\n")        
#                 break
# 	 #json.dump(MO_cases, f, sort_keys = True, indent = 4)
#   return filename 


def cases_MO(state_url):
  with requests.get(state_url) as r_state:
      cases=json.loads(r_state.text)
      for i in range(len(cases)): 
          if cases[i]['state']== 'MO': 
              MO_cases = cases[i]['positiveIncrease']
              #f.write('The number of new cases in Missouri are '+ "'"+str(MO_cases)+"'"+" on " +str( time) +"\n")        
              return MO_cases
              #break
	 #json.dump(MO_cases, f, sort_keys = True, indent = 4)


# def cases_zip(zip_url,filename=''):
#     if filename:
#         pass
#     else:
#         filename = cases_zip.txt
#     with requests.get(zip_url) as r_zip:
#        with open(filename,'a') as f:
#            cases = json.loads(r_zip.text)
#            for i in range(len(cases['features'])):
#                if cases['features'][i]['properties']['zip_5'] ==63146:
#                   f.write('The number of total cases in the zip code 63146 are '+ "'"+ str(cases['features'][i]['properties']['cases'])+ "'"+" on " +str( time)+"\n"*2)
#     return filename


# def cases_zip(zip_url):
#     with requests.get(zip_url) as r_zip:
#         cases = json.loads(r_zip.text)
#         for i in range(len(cases['features'])):
#             if cases['features'][i]['properties']['zip_5'] ==63146:
#                 #f.write('The number of total cases in the zip code 63146 are '+ "'"+ str(cases['features'][i]['properties']['cases'])+ "'"+" on " +str( time)+"\n"*2)
#                 return cases['features'][i]['properties']['cases']
#                 break


def cases_zip(zip_url):
    with requests.get(zip_url) as r_zip:
        cases = json.loads(r_zip.text)
        for i in range(len(cases['features'])):
            if cases['features'][i]['attributes']['zip_5'] ==63146:
                #f.write('The number of total cases in the zip code 63146 are '+ "'"+ str(cases['features'][i]['properties']['cases'])+ "'"+" on " +str( time)+"\n"*2)
                #{'zip_5': 63025, 'cases_total': 291, 'cases_new': 50, 'cases_new_youth': 0, 'population': 8369, 'population_youth': 2589, 'cases_total_100k': 3477.1, 'cases_new_100k': 597.4, 'cases_new_youth_100k': '0', 'ObjectId': 1}
                return cases['features'][i]['attributes']['cases_new']
                #break



# def cases_county(county_url, filename=''):
#     if filename:
#         pass
#     else:
#         filename= cases_county.txt
#     with requests.get(county_url) as r_county:
#         with open(filename,'a') as f:
#             cases=json.loads(r_county.text)
#             for i in range(len(cases['message'])):
#                 if cases['message'][i]['county_name']=='St. Louis':
#                     f.write('The number of new cases in St. Louis county are '+ "'"+str(cases['message'][i]['new'])+"'"+ " on "+ str( time)+ "\n")
#                     break
#    return filename



def cases_county(county_url):
    with requests.get(county_url) as r_county:
        cases=json.loads(r_county.text)
        for i in range(len(cases['message'])):
            if cases['message'][i]['county_name']=='St. Louis':
                #f.write('The number of new cases in St. Louis county are '+ "'"+str(cases['message'][i]['new'])+"'"+ " on "+ str( time)+ "\n")
                return cases['message'][i]['new']
                #break





# def case_MO(state_url,filename=''):
#    if filename:
#        pass
#    else:
#        filename = cases_MO.txt
#    with requests.get(state_url) as r_state:
#        with open(filename, 'a+') as f:
#           cases=json.loads(r_state.text)
#           csv_reader = csv.reader(f, delimiter=',') #to write and read into csv file
#           csv_writer = csv.writer(f)
#           dict_reader = csv.DictReader(f) # to read the coloumns
#           #coloumns= pd.read_csv(filename, nrows=1) #to get the header(1st row)
#           headers = dict_reader.fieldnames          
#           #rows  = list(csv_reader)   
#           df =  pd.DataFrame()
#           print(csv_reader )
#           print(df.Names)
#           for r in csv_reader:
#               print(r)
#               if r[0] == 'State': #:,'County','zip','Date':
#                  pass
#                   #print('state exists')
#               else:
#                  csv_writer.writerow(['State','County','Zip','Date'])
#           for i in range(len(cases)): 
#               if cases[i]['state']== 'MO':
#                  MO_cases = cases[i]['positiveIncrease']
#                  #f.write('The number of new cases in Missouri are '+ "'"+str(MO_cases)+"'"+" on " +str( time) +"\n")        
#                  csv_writer.writerow([MO_cases])
#                  break
#          #json.dump(MO_cases, f, sort_keys = True, indent = 4)
#    return filename 
def writer(filename):
    try:
        with open (filename, 'a') as f:
            csv_writer = csv.writer(f,lineterminator='\n')
            csv_writer.writerow([cases_MO(r_state), cases_county(r_county), cases_zip(r_zipcode),time])
            return filename
    except Exception:
        return None



condition = True
if condition:
    writer('cases.csv')
    condition = False


# Import data
if not condition:
    data = pd.read_csv('cases.csv', encoding = 'utf-8').fillna(0)



#data = pd.read_csv('cases.csv', encoding = 'utf-8').fillna(0)

zc = data['Zip'] .iloc[0:].values
county = data['County'] .iloc[0:].values
state = data['State'] .iloc[0:].values

hz = data.loc[data['Zip'] == max(zc), 'Date'].iloc[0]
hc = data.loc[data['County'] == max(county), 'Date'].iloc[0]
hs = data.loc[data['State'] == max(state), 'Date'].iloc[0]
#print('Highest number of new cases in MO state is on \'{}\' with \'{}\'\nHighest number of new cases in St.louis county is on \'{}\' with \'{}\'\nHighest number of new cases in 63146 Zip code is on \'{}\' with \'{}\'\n'.format(hs,max(state),hc,max(county),hz,max(zc)))

 
cases_today_zip =data.loc[data['Date'] == time, 'Zip'].iloc[0]
cases_today_state = data.loc[data['Date'] == time, 'State'].iloc[0]
cases_today_county = data.loc[data['Date'] == time, 'County'].iloc[0]

# Warning for zip code cases
if cases_today_zip== max(zc):
    print('ZipCode 63146 is in Danger Zone with maximum number of cases \'{}\'! Stay home and Stay safe!\nHighest number of new cases in 63146 Zip code recorded today \'{}\' with \'{}\'\n'.format(cases_today_zip,hz,max(zc)))
elif cases_today_zip >= dangerzone_zip:
    print('ZipCode 63146 is in Danger Zone with \'{}\' cases! Stay home and Stay safe!\nHighest number of new cases in 63146 Zip code was on \'{}\' with \'{}\'\n'.format(cases_today_zip,hz,max(zc)))
elif cases_today_zip <= safezone_zip:
    print('ZipCode 63146 is in Safe Zone with \'{}\' cases! Wear a mask and carry Sanitizer while going out.\nHighest number of new cases in 63146 Zip code was on \'{}\' with \'{}\'\n'.format(cases_today_zip,hz,max(zc)))
elif cases_today_zip > moderatezone_zip and cases_today_zip < dangerzone_zip:
    print('ZipCode 63146 is in Cautious Zone with \'{}\' cases! Wear a mask and carry Sanitizer  while going out.\nHighest number of new cases in 63146 Zip code was on \'{}\' with \'{}\'\n'.format(cases_today_zip,hz,max(zc)))
elif cases_today_zip > safezone_zip and cases_today_zip <= moderatezone_zip:
    print('ZipCode 63146 is in Moderate Zone with \'{}\' cases! Wear a mask and carry Sanitizer  while going out.\nHighest number of new cases in 63146 Zip code was on \'{}\' with \'{}\'\n'.format(cases_today_zip,hz,max(zc)))

# Warning for county cases
if cases_today_county== max(zc):
    print('St.Louis County is in Danger Zone with maximum number of cases \'{}\'! Stay home and Stay safe!\nHighest number of new cases in St.louis county recorded today \'{}\' with \'{}\'\n'.format(cases_today_zip),hc,max(county))
elif cases_today_county >= dangerzone_county:
    print('St.Louis County is in Danger Zone with \'{}\' cases! Stay home and Stay safe!\nHighest number of new cases in St.louis county was on \'{}\' with \'{}\'\n'.format(cases_today_county,hc,max(county)))
elif cases_today_county <= safezone_county:
    print('St.Louis County  is in Safe Zone with \'{}\' cases! Wear a mask and carry Sanitizer while going out.\nHighest number of new ca ses in St.louis county was on \'{}\' with \'{}\'\n'.format(cases_today_county,hc,max(county)))
elif cases_today_county > moderatezone_county and cases_today_county < dangerzone_county:
    print('St.Louis County  is in Cautious Zone with \'{}\' cases! Wear a mask and carry Sanitizer  while going out.\nHighest number of new cases in St.louis county was on \'{}\' with \'{}\'\n'.format(cases_today_county,hc,max(county)))
elif cases_today_county > safezone_county and cases_today_county <= moderatezone_county:
    print('St.Louis County  is in Moderate Zone with \'{}\' cases! Wear a mask and carry Sanitizer  while going out.\nHighest number of new cases in St.louis county was on \'{}\' with \'{}\'\n'.format(cases_today_county,hc,max(county)))

#print(max(zc),max(county),max(state))

# Warning for State cases
if cases_today_state == max(zc):
    print('Missouri state is in Danger Zone with maximum number of cases \'{}\'! Stay home and Stay safe!\nHighest number of new cases in MO state recorded today \'{}\' with \'{}\'\n'.format(cases_today_state),hs,max(state))
elif cases_today_state >= dangerzone_state:
    print('Missouri state is in Danger Zone with \'{}\' cases! Stay home and Stay safe!\nHighest number of new cases in MO state was on \'{}\' with \'{}\'\n'.format(cases_today_state,hs,max(state)))
elif cases_today_state<= safezone_state:
    print('Missouri state is in Safe Zone with \'{}\' cases! Wear a mask and carry Sanitizer while going out.\nHighest number of new cases in MO state was on \'{}\' with \'{}\'\n'.format(cases_today_state,hs,max(state)))
elif cases_today_state > moderatezone_state and cases_today_state < dangerzone_state:
    print('Missouri state  is in Cautious Zone with \'{}\' cases! Wear a mask and carry Sanitizer while going out.\nHighest number of new cases in MO state was on \'{}\' with \'{}\'\n'.format(cases_today_state,hs,max(state)))
elif cases_today_state > safezone_state and cases_today_state <= moderatezone_state:
    print('Missouri state  is in Moderate Zone with \'{}\' cases! Wear a mask and carry Sanitizer while going out.\nHighest number of new cases in MO state was on \'{}\' with \'{}\'\n'.format(cases_today_state,hs,max(state)))



# Graph plottinf=g
x = data['Zip'] #.iloc[0:10].values
y = data['Date'] #.iloc[0:10].values
z = data['County']
s = data['State']

fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
fig.suptitle('Plot of historic covid-19 data till today', color='crimson', fontname="Times New Roman",fontweight="bold")
ax1.plot(y, x, color='mediumvioletred')
ax1.legend(['Zipcode: 63146'])
ax1.xaxis.set_tick_params(rotation=18, labelsize=10)


ax2.plot(y,z,color='blue')
ax2.legend(['County'])
ax2.xaxis.set_tick_params(rotation=18, labelsize=10)

ax3.plot(y,s,color='brown')
ax3.legend(['Missouri'])
ax3.xaxis.set_tick_params(rotation=18, labelsize=10)

for ax in (ax1, ax2, ax3):
    ax.set(xlabel='Dates', ylabel='New Covid-19 cases daily')

plt.show()
# #fig.savefig("plot.png")

















#case_MO(r_state,'statecases.csv')
#cases_MO(r_state,'testing_statecases.txt')
#cases_county(r_county,'testing_statecases.txt')
#cases_zip(r_zipcode,'testing_statecases.txt')

#x = json.loads(r_county.text)
#print(type(x))
#print(x)
#for i in range(len(x['features'])):
#	if x['features'][i] ['properties']['zip_5'] ==63146:
#		print('The number of total cases in the zip code 63146 are '+ "'"+ str(x['features'][i]['properties']['cases'])+ "'")


