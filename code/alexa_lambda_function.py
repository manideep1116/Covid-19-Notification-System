import json
import datetime
import pandas as pd
import boto3


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

#Covid_bucket = os.environ['bucket']
Covid_bucket = 'covid-project-testing'
s3 = boto3.resource('s3')
bucket = s3.Bucket(Covid_bucket)
key = 'cases.csv'
SKILL_NAME = "Covid nineteen prevention"

def lambda_handler(event, context):
    local_file = '/tmp/covid_cases.csv'
    s3.Bucket(Covid_bucket).download_file(key,local_file)
    session  = event['session']
    print(json.dumps(event))
    if event['request']['type']== "LaunchRequest":
        return on_launch_request(event['request'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent_request(event['request'],local_file)
    elif event['request']['type'] == "SessionEndedRequest":
        return ()

def on_intent_request(intent_request,local_file):
    intent =  intent_request['intent']
    intent_name = intent_request['intent']['name']
    if intent_name == "hellointent":
        return handle_hello_intent(intent)
    elif intent_name == "CovidIntent":
        return handle_covid_intent(intent,local_file)
   
    elif intent_name == "MissouriIntent":
        return handle_missouri_intent(intent, local_file)
    elif intent_name ==  "SaintLouisCountyIntent":
        return handle_saint_louis_intent(intent, local_file)
    elif intent_name == "ZipCodeIntent":
        return handle_zipcode_intent(intent,local_file)

    elif intent_name == "SurgeIntent":
        return handle_mo_surge_intent(intent, local_file)
    else:
        raise ValueError("unknown intent")

def on_launch_request(launch_request):
    options = {}
    options["SpeechText"] = "Welcome to Manideep's Covid nineteen prevention skill. Life is precious, be vigilant and use this project for your safety.  "
    options["repromptText"] = "What do you want to know? For example you can ask for covid nineteen cases in Saint louis county or in zip code 63146. "
    options["endSession"] =  False
    return build_response(options)
    # options["SpeechText"] = ("Welcome to Manideep's {}. Find out covid nineteen data around you in Missouri. ".format(SKILL_NAME))
    # options["reprompText"] = "Find out covid nineteen data in Missouri. For example you can ask to get the number of cases in Saint louis county today. "

def handle_covid_intent(intent, local_file):
    options={}
    data = pd.read_csv(local_file, encoding = 'utf-8').fillna(0)


    zc = list(data['Zip'] .iloc[0:].values)
    county = list(data['County'] .iloc[0:].values)
    state = list(data['State'] .iloc[0:].values)
      # Warning for zip code cases
    today_zip = int(zc[-1])
    today_county = int(county[-1])
    today_state = int(state[-1])
    if today_zip  == max(zc):
        zip_cases='ZipCode six three one four six is in Danger Zone with maximum number of new cases "'+ str(today_zip) + '" today. Stay home and Stay safe!'
    elif today_zip>= dangerzone_zip:
         zip_cases='ZipCode six three one four six is in Danger Zone with "'+ str(today_zip) + '" new cases ! Stay home and Stay safe!'
    elif today_zip<= safezone_zip:
        zip_cases='ZipCode six three one four six is in Safe Zone with "' + str(today_zip) + '" new cases!  Wear a mask and carry Sanitizer while going out.'
    elif today_zip> moderatezone_zip and today_zip < dangerzone_zip:
        zip_cases='ZipCode six three one four six is in Cautious Zone with "' + str(today_zip) + '" new cases !  Wear a mask and carry Sanitizer while going out.'
    elif today_zip > safezone_zip and today_zip<= moderatezone_zip:
        zip_cases='ZipCode six three one four six is in Moderate Zone with  "' + str(today_zip) + '" new cases !  Wear a mask and carry Sanitizer while going out.'

        # Warning for county cases
    if today_county== max(county):
        county_cases='Saint Louis County is in Danger Zone with maximum number of new cases "' + str(today_county) +'" today. Stay home and Stay safe!'
    elif today_county >= dangerzone_county:
        county_cases='Saint Louis  County is in Danger Zone with "'+ str(today_county) + '" new cases! Stay home and Stay safe!'
    elif today_county <= safezone_county:
        county_cases='Saint Louis  County  is in Safe Zone with "' + str(today_county)+ '" new cases!  Wear a mask and carry Sanitizer while going out.'
    elif today_county > moderatezone_county and today_county < dangerzone_county:
        county_cases='Saint Louis  County  is in Cautious Zone with  "' + str(today_county) + '" new cases!  Wear a mask and carry Sanitizer while going out.'
    elif today_county > safezone_county and today_county <= moderatezone_county:
        county_cases='Saint Louis  County is in Moderate Zone with  "' + str(today_county) + '" new cases!  Wear a mask and carry Sanitizer while going out.'

    

        # Warning for State cases
    if today_state == max(state):
        state_cases='Missouri state is in Danger Zone with maximum number of new cases "'+ str(today_state) + '" today. Stay home and Stay safe!'
    elif today_state >= dangerzone_state:
        state_cases='Missouri state is in Danger Zone with "'+ str(today_state) + '" new cases! Stay home and Stay safe!'
    elif today_state<= safezone_state:
        state_cases='Missouri state is in Safe Zone with  "' + str(today_state) + '" new cases!  Wear a mask and carry Sanitizer while going out.'
    elif today_state > moderatezone_state and today_state < dangerzone_state:
        state_cases='Missouri state  is in Cautious Zone with  "' + str(today_state) + '" new cases!  Wear a mask and carry Sanitizer while going out.'
    elif today_state > safezone_state and today_state <= moderatezone_state:
        state_cases='Missouri state  is in Moderate Zone with  "' + str(today_state) + '" new cases!  Wear a mask and carry Sanitizer while going out.'
    
    
    #
    if ('value' in intent['slots']['zone'] and 'value' in intent['slots']['MO']) or ('value' in intent['slots']['MO']) :
        options["SpeechText"]= "Here is the data from Manideep's covid prevention project, "+ state_cases
    elif ('value' in intent['slots']['zone'] and 'value' in intent['slots']['county']) or ('value' in intent['slots']['county']):
        options["SpeechText"]= "Here is the data from Manideep's covid prevention project, "+ county_cases
    elif ('value' in intent['slots']['zone'] and 'value' in intent['slots']['zip']) or ('value' in intent['slots']['zip']):
        options["SpeechText"]= "Here is the data from Manideep's covid prevention project, "+ zip_cases  
    elif ('value' in intent['slots']['zone']):
        options["SpeechText"]= "Here is the data from Manideep's covid prevention project, "+ zip_cases  
    else:
        options["SpeechText"]= "Here is the data from Manideep's covid prevention project, Covid cases in Missouri are {}, cases in Saint Louis County are {}, and number of covid nineteen cases in your zipcode six three one four six are {}. Wear a mask while going out! ".format(state[-1], county[-1], zc[-1])

   
    #
    options["endSession"] = False
    options["cardTitle"] = "hello {}. ".format(SKILL_NAME)
    options["cardContent"] = options["SpeechText"] 
    options["repromptText"] = "How can I help you with knowing more about covid cases around you?"
    return build_response(options)
# //////////// intents for number of cases
def handle_missouri_intent(intent, local_file):
    options = {}
    
    if 'value' in intent['slots']['number']:
        num = int(intent['slots']["number"]["value"])
    else:
        num = 0
    
    data = pd.read_csv(local_file, encoding = 'utf-8').fillna(0)
    state = list(data['State'] .iloc[0:].values)
    if num == 1 or num ==0:
        options["SpeechText"] = "Here is the data from Manideep's covid prevention project, today's Covid cases in Missouri are {}. ".format(state[-1])
    else:
        cases = ""
        for i in state[-num:]: cases+=str(i)+", "
        options["SpeechText"] = "Here is the data from Manideep's covid prevention project, daily new Covid cases in Missouri for last {} days are {}. ".format(num,cases)
    options["endSession"] = False
    options["cardTitle"] = "hello {}. ".format(SKILL_NAME)
    options["cardContent"] = options["SpeechText"] 
    options["repromptText"] = "How can I help you with knowing more about covid nineteen prevention and situation in your state Missouri? "
            
    return build_response(options)


def handle_saint_louis_intent(intent, local_file):
    options = {}
    if 'value' in intent['slots']['number']:
        num = int(intent['slots']["number"]["value"])
    else:
        num = 0
    
    data = pd.read_csv(local_file, encoding = 'utf-8').fillna(0)
    county = list(data['County'] .iloc[0:].values)
    if num == 1 or num ==0:
        options["SpeechText"] = "Here is the data from Manideep's covid prevention project, today's Covid cases in Saint Louis county are {}. ".format(county[-1])
    else:
        cases = ""
        for i in county[-num:]: cases+=str(i)+", "
        options["SpeechText"] = "Here is the data from Manideep's covid prevention project, daily new ovid cases in Saint Louis County for last {} days are {}. ".format(num,cases)
    options["endSession"] = False
    options["cardTitle"] = "hello {}. ".format(SKILL_NAME)
    options["cardContent"] = options["SpeechText"] 
    options["repromptText"] = "How can I help you with knowing more about covid nineteen prevention and situation in the Saint Louis county "
    return build_response(options)

def handle_zipcode_intent(intent, local_file):
    options = {}
    if 'value' in intent['slots']['number']:
        num = int(intent['slots']["number"]["value"])
    else:
        num = 0
    
    data = pd.read_csv(local_file, encoding = 'utf-8').fillna(0)
    Zip = list(data['Zip'] .iloc[0:].values)
    if num == 1 or num ==0:
        options["SpeechText"] = "Here is the data from Manideep's covid prevention project, today's Covid cases in zip code six three one four six {}. ".format(Zip[-1])
    else:
        cases = ""
        for i in Zip[-num:]: cases+=str(i)+", "
        options["SpeechText"] = "Here is the data from Manideep's covid prevention project, daily new Covid cases in zip code six three one four six for last {} days are {}. ".format(num,cases)
    options["endSession"] = False
    options["cardTitle"] = "hello {}. ".format(SKILL_NAME)
    options["cardContent"] = options["SpeechText"] 
    options["repromptText"] = "How can I help you with knowing more about covid nineteen prevention and situation in your zip code six three one four six? "
    return build_response(options)
    
    

def handle_mo_surge_intent(intent, local_file):
    options={}
    data = pd.read_csv(local_file, encoding = 'utf-8').fillna(0)
    Zip = list(data['Zip'] .iloc[0:].values) 
    county = list(data['County'] .iloc[0:].values)
    state = list(data['State'] .iloc[0:].values)
    
     #
    if ('value' in intent['slots']['MO']):
        if int(state[-1]-state[-2]) > 0 :
            options["SpeechText"]= "Here is the data from Manideep's covid prevention project, there is a surge of {} cases in Missouiri today with {} new cases today. ".format(int(state[-1]-state[-2]),state[-1])
        elif int(state[-1]-state[-2]) < 0:
            options["SpeechText"] ="Here is the data from Manideep's covid prevention project, there is decrease in {} Covid cases in Missouri with {} new cases today. ".format(int(state[-2]-state[-1]),state[-1]) 
        else:
            options["SpeechText"] ="Here is the data from Manideep's covid prevention project, there is no surge in the Covid cases in Missouri" 
    
    elif ('value' in intent['slots']['county']):
        if int(county[-1]-county[-2]) > 0 :
            options["SpeechText"]= "Here is the data from Manideep's covid prevention project, there is a surge of {} cases in Saint Louis county today with {} new cases today. ".format(int(county[-1]-county[-2]),county[-1])
        elif int(county[-1]-county[-2]) < 0:
            options["SpeechText"] ="Here is the data from Manideep's covid prevention project, there is decrease in {} new Covid cases in Saint Louis county with {} new cases today. ".format(int(county[-2]-county[-1]),county[-1]) 
        else:
            options["SpeechText"] ="Here is the data from Manideep's covid prevention project, there is no surge in the Covid cases in Saint Louis county" 
   
    else:
        if int(Zip[-1]-Zip[-2]) > 0 :
            options["SpeechText"]= "Here is the data from Manideep's covid prevention project, there is a surge of {} cases in zip code six three one four six today with {} new cases today. ".format(int(Zip[-1]-Zip[-2]),Zip[-1])
        elif int(Zip[-1]-Zip[-2]) < 0:
            options["SpeechText"] ="Here is the data from Manideep's covid prevention project, there is decrease in {} Covid cases in zip code six three one four six with {} new cases today. ".format(int(Zip[-2]-Zip[-1]),Zip[-1]) 
        else:
            options["SpeechText"] ="Here is the data from Manideep's covid prevention project, there is no surge in the Covid cases in zip code six three one four six " 

    options["endSession"] = False
    options["cardTitle"] = "hello {}. ".format(SKILL_NAME)
    options["cardContent"] = options["SpeechText"] 
    options["repromptText"] = "How can I help you with knowing more about covid cases around you?"
    return build_response(options)



def handle_hello_intent(intent):
    options={}
    name = intent['slots']["Firstname"]["value"]
    options["SpeechText"] = "Welcome {} ".format(name)
    options["SpeechText"]+= get_wish()
    options["endSession"] = True
    options["cardTitle"] = "hello {}. ".format(name)
    options["cardContent"] = "Get a Wish"
    options["repromptText"] = "How can I help you?"
    return build_response(options)

def get_wish():
    time = datetime.datetime.utcnow() 
    hours = time.hour - 6
    if hours < 0:
        hours += 24

    if hours < 12:
        return "Good Morning. "
    elif hours < 18:
        return "Good Afternoon. "
    else:
        return "Good Evening. "
    



def build_response(options):
    response={
    "version": "1.0",
    "response": {
        "outputSpeech": {
            "type": "PlainText",
            "text": options["SpeechText"]
    },
    "shouldEndSession": options["endSession"]
    }}
    if "repromptText" in options.keys():
        response["response"]["reprompt"]={
            "outputSpeech": {
                "type": "PlainText",
                "text": options["repromptText"]
      }

        }
    if (("session" in options.keys()) and ("attributes" in options["session"])):
        response["sessionAttributes"] == options["session"]["attributes"]
    
    if "cardTitle" in options.keys():
        response["card"]={
            "type": "Simple",
            "title": options["cardTitle"],
            "content": options["SpeechText"]
        }
    return response


