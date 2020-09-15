import requests
import json
import csv  
from datetime import datetime, date
import pandas as pd

r_county = 'https://covid19-us-api.herokuapp.com/county'
r_zipcode = 'https://opendata.arcgis.com/datasets/7ad849e453684ea09f92ac56bd97a08e_0.geojson'
#r_state =  'https://covidtracking.com/api/states'
r_state = 'https://covidtracking.com/api/states/daily'
now = datetime.now()
today = date.today()
time = today.strftime("%m/%d/%y")

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
              break
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


def cases_zip(zip_url):
    with requests.get(zip_url) as r_zip:
        cases = json.loads(r_zip.text)
        for i in range(len(cases['features'])):
            if cases['features'][i]['properties']['zip_5'] ==63146:
                #f.write('The number of total cases in the zip code 63146 are '+ "'"+ str(cases['features'][i]['properties']['cases'])+ "'"+" on " +str( time)+"\n"*2)
                return cases['features'][i]['properties']['cases']
                break






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
                break





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



writer('cases.csv')

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


