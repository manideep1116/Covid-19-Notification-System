import requests
import json
import csv  
from datetime import datetime, date
import pandas as pd
import boto3
import os





# Access environment variables from SAM template
Covid_bucket = os.environ['bucket']
sns_smsARN = os.environ['sns_sms']
r_county = os.environ['County_url']
r_zipcode = os.environ['Zip_url']
r_state = os.environ['MO_url']

zip_cases=''
county_cases=''
state_cases=''

s3 = boto3.resource('s3')
bucket = s3.Bucket(Covid_bucket)
key = 'cases.csv'



now = datetime.now()
today = date.today()
time = today.strftime("%m/%d/%y")
message = ''

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



def cases_MO(state_url):
    '''
    parameter: URL with Covid-19 data for States in USA
    output: Number of daily new covid-19 cases in Missouri
    '''
    with requests.get(state_url) as r_state:
        cases=json.loads(r_state.text)
        for i in range(len(cases)): 
            if cases[i]['state']== 'MO': 
                MO_cases = cases[i]['positiveIncrease']
               #f.write('The number of new cases in Missouri are '+ "'"+str(MO_cases)+"'"+" on " +str( time) +"\n")        
                return MO_cases



def cases_zip(zip_url):
    '''
    parameter: URL with Covid-19 data for ZipCodes in Missouri
    output: Number of daily new covid-19 cases in ZipCode 63146
    '''
    with requests.get(zip_url) as r_zip:
        cases = json.loads(r_zip.text)
        for i in range(len(cases['features'])):
            if cases['features'][i]['attributes']['zip_5'] ==63146:
                #f.write('The number of total cases in the zip code 63146 are '+ "'"+ str(cases['features'][i]['properties']['cases'])+ "'"+" on " +str( time)+"\n"*2)
                #{'zip_5': 63025, 'cases_total': 291, 'cases_new': 50, 'cases_new_youth': 0, 'population': 8369, 'population_youth': 2589, 'cases_total_100k': 3477.1, 'cases_new_100k': 597.4, 'cases_new_youth_100k': '0', 'ObjectId': 1}
                return cases['features'][i]['attributes']['cases_new']
                


def cases_county(county_url):
    '''
    parameter: URL with Covid-19 data for Counties in USA
    output: Number of daily new covid-19 cases in St. Louis County
    '''
    with requests.get(county_url) as r_county:
        cases=json.loads(r_county.text)
        for i in range(len(cases['message'])):
            if cases['message'][i]['state_name']== "Missouri" and cases['message'][i]['county_name']=='St. Louis':
                #f.write('The number of new cases in St. Louis county are '+ "'"+str(cases['message'][i]['new'])+"'"+ " on "+ str( time)+ "\n")
                return cases['message'][i]['new']


def notification(text):
    '''
    parameters: Text message to SNS Subscriber
    '''
    try:
        sns = boto3.client('sns')
        sns.publish(TopicArn = sns_smsARN, Message = text)
    except Exception as e:
        print("Failed to sent the SMS with the reason {}".format(e))
        exit(1)




def lambda_handler(event, context):    
    lamba_local_file = '/tmp/covid_cases.csv'
    s3.Bucket(Covid_bucket).download_file(key,lamba_local_file)
    try:
        with open (lamba_local_file, 'a') as f:
            csv_writer = csv.writer(f,lineterminator='\n')
            csv_writer.writerow([cases_MO(r_state), cases_county(r_county), cases_zip(r_zipcode),time])
            
        data = pd.read_csv(lamba_local_file, encoding = 'utf-8').fillna(0)

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
            zip_cases='ZipCode 63146 is in Danger Zone with maximum number of new cases "'+ str(cases_today_zip) + '" today. Stay home and Stay safe!'
        elif cases_today_zip >= dangerzone_zip:
            zip_cases='ZipCode 63146 is in Danger Zone with "'+ str(cases_today_zip) + '" new cases ! Stay home and Stay safe!'
        elif cases_today_zip <= safezone_zip:
            zip_cases='ZipCode 63146 is in Safe Zone with "' + str(cases_today_zip) + '" new cases!  Wear a mask and carry Sanitizer while going out.'
        elif cases_today_zip > moderatezone_zip and cases_today_zip < dangerzone_zip:
            zip_cases='ZipCode 63146 is in Cautious Zone with "' + str(cases_today_zip) + '" new cases !  Wear a mask and carry Sanitizer while going out.'
        elif cases_today_zip > safezone_zip and cases_today_zip <= moderatezone_zip:
            zip_cases='ZipCode 63146 is in Moderate Zone with  "' + str(cases_today_zip) + '" new cases !  Wear a mask and carry Sanitizer while going out.'

        # Warning for county cases
        if cases_today_county== max(county):
            county_cases='St.Louis County is in Danger Zone with maximum number of new cases "' + str(cases_today_county) +'" today. Stay home and Stay safe!'
        elif cases_today_county >= dangerzone_county:
            county_cases='St.Louis County is in Danger Zone with "'+ str(cases_today_county) + '" new cases! Stay home and Stay safe!'
        elif cases_today_county <= safezone_county:
            county_cases='St.Louis County  is in Safe Zone with "' + str(cases_today_county)+ '" new cases!  Wear a mask and carry Sanitizer while going out.'
        elif cases_today_county > moderatezone_county and cases_today_county < dangerzone_county:
            county_cases='St.Louis County  is in Cautious Zone with  "' + str(cases_today_county) + '" new cases!  Wear a mask and carry Sanitizer while going out.'
        elif cases_today_county > safezone_county and cases_today_county <= moderatezone_county:
            county_cases='St.Louis County  is in Moderate Zone with  "' + str(cases_today_county) + '" new cases!  Wear a mask and carry Sanitizer while going out.'

        #print(max(zc),max(county),max(state))

        # Warning for State cases
        if cases_today_state == max(state):
            state_cases='Missouri state is in Danger Zone with maximum number of new cases "'+ str(cases_today_state) + '" today. Stay home and Stay safe!'
        elif cases_today_state >= dangerzone_state:
            state_cases='Missouri state is in Danger Zone with "'+ str(cases_today_state) + '" new cases! Stay home and Stay safe!'
        elif cases_today_state<= safezone_state:
            state_cases='Missouri state is in Safe Zone with  "' + str(cases_today_state) + '" new cases!  Wear a mask and carry Sanitizer while going out.'
        elif cases_today_state > moderatezone_state and cases_today_state < dangerzone_state:
            state_cases='Missouri state  is in Cautious Zone with  "' + str(cases_today_state) + '" new cases!  Wear a mask and carry Sanitizer while going out.'
        elif cases_today_state > safezone_state and cases_today_state <= moderatezone_state:
            state_cases='Missouri state  is in Moderate Zone with  "' + str(cases_today_state) + '" new cases!  Wear a mask and carry Sanitizer while going out.'
        
        notification(" Covid-19 Prevention Message from Manideep :)\n\nLife is precious, be careful and follow this message before you step out!\n\n{}\n\n{}\n\n{}".format(zip_cases, county_cases, state_cases))
        #email()
        bucket.upload_file(lamba_local_file , key)
        return {
            'message': 'success!!'
            }
    except Exception:
        return None



#https://covidtracking.com/data/download
#https://covidti.com/api/public/us/timeseries/Missouri/St.%20louis for county
# r_zipcode = 'https://opendata.arcgis.com/datasets/7ad849e453684ea09f92ac56bd97a08e_0.geojson'
#https://data-stlcogis.opendata.arcgis.com/datasets/covid-19-zip-code-data-w-past-14-days/geoservice?page=5&selectedAttribute=cases_new
#r_state =  'https://covidtracking.com/api/states'

# r_county = 'https://covid19-us-api.herokuapp.com/county'
# r_zipcode = "https://services2.arcgis.com/w657bnjzrjguNyOy/arcgis/rest/services/covid19_by_zip_expanded_1/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"
# r_state = 'https://covidtracking.com/api/states/daily'