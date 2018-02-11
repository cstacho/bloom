import get_opps
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
    result = get_opps.get_opportunities()
    if intent_request['sessionAttributes'] and intent_request['confirmationStatus'] == 'Confirmed':
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                     "contentType": "PlainText",
                     "content": "Thank you! We've signed you up for " + intent_request['sessionAttributes']['opp'] + " on " + intent_request['slots']['DayOfWeek'] + ". Thank you for helping women bloom!"
                },
            }
        }
    else:
        return { 
            "dialogAction": {
                "type": "dialogAction",
                "message": {
                     "contentType": "PlainText",
                     "content": "How about volunteering with " + result["name"] +"?" + " " + result["description"]
                 },
                 "intentName": "Volunteer",
                 "slots": intent_request['slots']
                 ,
                 }
                 ,
                 "sessionAttributes": { 
                    "opp": result["name"]
                    }
            }
    

def alexa_opp_info(intent_request, session):
    card_title = "vol"
    session_attributes = {}
    should_end_session = False
    intent = intent_request['request']['intent']
    dialog_state = intent_request['request']['dialogState']
    if dialog_state == 'STARTED':
        return {
            'version': '1.0',
            'sessionAttributes': session_attributes,
            'response': {
                "directives": [
                    {
                        "type": "Dialog.Delegate"
                    }],
                "shouldEndSession": False
              
              }
            }
            
    elif dialog_state != 'COMPLETED':
        return {
          'version': '1.0',
            'sessionAttributes': session_attributes,
            'response': {
                "directives": [
                    {
                        "type": "Dialog.Delegate"
                    }],
                "shouldEndSession": False
              
              }
            }
    else:
        return alexa_volunteer(intent_request, session)

def location(loc):
    return {"Location": loc}    
    
def alexa_volunteer(intent_request, session):
    result = get_opps.get_opportunities()
    should_end_session = False
    card_title = result["name"]
    
    if not session['attributes']:
         return {
          "version": "1.0",
          "sessionAttributes": { "opp": result['name']},
          "response": {
            "outputSpeech": {
              "type": "PlainText",
              "text": "How about" + result['name'] + "?" + result['description']
            },
            "directives": [{
                "type": "Dialog.ConfirmIntent"
            }],
            "shouldEndSession": False
            }
        }
        
    speech_output = "Great! You're all signed up."
    shouldEndSession = True
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
    
def volunteer(intent_request):
    if intent_request['type'] == 'bot':
        return build_bot_response(intent_request)


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.

    """
    intent_name = intent_request['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'Volunteer':
        return volunteer(intent_request)

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

    print("on_intent requestId=" + intent_request['request']['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['request']['intent']
    intent_name = intent_request['request']['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "Volunteer":
        return alexa_opp_info(intent_request, session)
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
    else:
        print("event.session.application.applicationId=" + event['session']['application']['applicationId'])
        
        if event['session']['new']:
            on_session_started({'requestId': event['request']['requestId']}, event['session'])
        
        if event['request']['type'] == "LaunchRequest":
            return on_launch(event['request'], event['session'])                   
        elif event['request']['type'] == "IntentRequest":
            return on_intent(event, event['session'])
        elif event['request']['type'] == "SessionEndedRequest":
            return on_session_ended(event['request'], event['session'])
        else:
            raise ValueError("Invalid intent")
        """
        intent_request = {'name': event['request']['intent']['name'], 'slots': event['request']['intent']['slots'], 'sessionAttributes': event['session']['attributes'], 'type': 'echo'}
        """    
    return dispatch(intent_request)
    
