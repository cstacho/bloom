import people
import logging
import time
import os
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
    
def build_bot_response(intent_request):
    date = people.date()
    skill = intent_request["slots"]["Skill"].lower()
    city= intent_request["slots"]["City"]
    state = intent_request["slots"]["State"]
    match = people.get_mentor(skill)
    if intent_request['sessionAttributes'] and intent_request['confirmationStatus'] == 'Confirmed':
        match = intent_request["sessionAttributes"]["match"] 
        email = intent_request["sessionAttributes"]["match"].replace(" ","").lower() + "@gmail.com"
        date = intent_request["sessionAttributes"]["date"] 
        return { 
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                         "contentType": "PlainText",
                         "content": "Okay, Reach out to "+match + " at " + email+ " . "+match + " is so excited to meet with you next " + date+". Type another command to use another feature"
                     }
                     }
                }
    else:
        return { 
            "dialogAction": {
                "type": "ConfirmIntent",
                "message": {
                     "contentType": "PlainText",
                     "content": "We've matched you with " + match + ". We've expertly crafted this match in " + skill.capitalize()+ " and we can't wait for the both of you to meet in " + city + ", " + state +". After analyzing your calender, how about meeting next " + date+ "?" 
                 },
                 "intentName": "Connect",
                 "slots": intent_request['slots']
                 ,
                 }
                 ,
                 "sessionAttributes": { 
                    "match": match,
                    "date": date
                    }
            }
    
                         
    
def connect(intent_request):
    if intent_request['type'] == 'bot':
        return build_bot_response(intent_request)
    else:
       return alexa_volunteer(intent_request, intent_request['session'])


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.

    """
    intent_name = intent_request['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'Connect':
        return connect(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
  
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Bloom, where women grow together. " \
                   "Would you like to volunteer, discover, donate or connect?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me if you would like to volunteer, " \
                    "or discover"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()
    
def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "Connect":
        return alexa_opp_info(intent, session)
    elif intent_name == "WhatsMyColorIntent":
        return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
          
def lambda_handler(event, context):
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    print(event)
    
    if 'currentIntent' in event:
        intent_request = {'name': event['currentIntent']['name'], 'slots': event['currentIntent']['slots'], 'sessionAttributes': event['sessionAttributes'], 'confirmationStatus': event['currentIntent']['confirmationStatus'], 'type': 'bot'}

    return dispatch(intent_request)
    