import requests
import json
import csv  
from datetime import datetime
import pandas as pd

r_county = 'https://covid19-us-api.herokuapp.com/county'
r_zipcode = 'https://opendata.arcgis.com/datasets/7ad849e453684ea09f92ac56bd97a08e_0.geojson'
#r_state =  'https://covidtracking.com/api/states'
r_state = 'https://covidtracking.com/api/states/daily'
now = datetime.now()
time = now.strftime("%d/%m/%Y %H:%M:%S")


def case_MO(state_url,filename=''):
   if filename:
       pass
   else:
       filename = cases_MO.txt
   with requests.get(state_url) as r_state:
       with open(filename, 'a+') as f:
          cases=json.loads(r_state.text)
          csv_reader = csv.reader(f, delimiter=',') #to write and read into csv file
          csv_writer = csv.writer(f)
          dict_reader = csv.DictReader(f) # to read the coloumns
          #coloumns= pd.read_csv(filename, nrows=1) #to get the header(1st row)
          headers = dict_reader.fieldnames          
          #rows  = list(csv_reader)   
          #df =  pd.DataFrame()
          #print(csv_reader )
          #for r in csv_reader:
              #print(r)
          if  headers ==  ['State','County','zip','Date']:
            pass
          else:
            csv_writer.writerow(['State','County','Zip','Date'])
          for i in range(len(cases)): 
              if cases[i]['state']== 'MO':
                 MO_cases = cases[i]['positiveIncrease']
                 #f.write('The number of new cases in Missouri are '+ "'"+str(MO_cases)+"'"+" on " +str( time) +"\n")        
                 csv_writer.writerow([MO_cases])
                 break
         #json.dump(MO_cases, f, sort_keys = True, indent = 4)
   return filename 

case_MO(r_state,'statecases1.csv')
