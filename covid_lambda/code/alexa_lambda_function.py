import json
import datetime
import pandas as pd
import boto3

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
    elif intent_name ==  "SaintLouisIntent":
        return handle_saint_louis_intent(intent, local_file)
    elif intent_name == "ZipCodeIntent":
        return handle_zipcode_intent(intent,local_file)
    else:
        raise ValueError("unknown intent")

def handle_missouri_intent(intent, local_file):
    options = {}
    
    if 'value' in intent['slots']:
        num = int(intent['slots']["number"]["value"])
    else:
        num = 0
    
    data = pd.read_csv(local_file, encoding = 'utf-8').fillna(0)
    state = list(data['State'] .iloc[0:].values)
    if num == 1 or num ==0:
        options["SpeechText"] = "Here is the data from Manideep's covid prevention project, today's Covid cases in Missouri are {}. ".format(state[-1])
    else:
        cases = ""
        for i in state[-num:]: cases+=str(i)+" "
        options["SpeechText"] = "Here is the data from Manideep's covid prevention project, Covid cases in Missouri for last {} days are {}. ".format(num,cases)
    options["endSession"] = False
    options["cardTitle"] = "hello {}. ".format(SKILL_NAME)
    options["cardContent"] = options["SpeechText"] 
    options["repromptText"] = "How can I help you with knowing more about covid cases around you?"
            
    return build_response(options)


def handle_saint_louis_intent(intent, local_file):
    options = {}
    return build_response(options)

def handle_zipcode_intent(intent, local_file):
    options = {}
    return build_response(options)

def handle_covid_intent(intent, local_file):
    options={}
    data = pd.read_csv(local_file, encoding = 'utf-8').fillna(0)

    zc = list(data['Zip'] .iloc[0:].values)
    county = list(data['County'] .iloc[0:].values)
    state = list(data['State'] .iloc[0:].values)
    options["SpeechText"] = "Here is the data from Manideep's covid prevention project, Covid cases in Missouri are {}, cases in Saint Louis County are {}, and number of covid nineteen cases in your zipcode six three one four six are {}".format(state[-1], county[-1], zc[-1])
    options["endSession"] = False
    options["cardTitle"] = "hello {}. ".format(SKILL_NAME)
    options["cardContent"] = options["SpeechText"] 
    options["repromptText"] = "How can I help you with knowing more about covid cases around you?"
            
    
    return build_response(options)

def handle_mo_zone_intent(intent, local_file):
    options={}
    return build_response(options)

def handle_zipcode_zone_intent(intent, local_file):
    options={}
    return build_response(options)

def handle_county_zone_intent(intent, local_file):
    options={}
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
    


def on_launch_request(launch_request):
    options = {}
    options["SpeechText"] = "Welcome to Manideep's Covid nineteen prevention skill. "
    options["repromptText"] = "What do you want to know? For example you can ask for covid nineteen cases in Saint louis county or in zip code 63146. "
    options["endSession"] =  False
    return build_response(options)
    # options["SpeechText"] = ("Welcome to Manideep's {}. Find out covid nineteen data around you in Missouri. ".format(SKILL_NAME))
    # options["reprompText"] = "Find out covid nineteen data in Missouri. For example you can ask to get the number of cases in Saint louis county today. "
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


