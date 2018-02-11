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
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                     "contentType": "PlainText",
                     "content": "Thanks for helping women grow! See you soon. "
                },
            }
        }
    
def goodbye(intent_request):
    if intent_request['type'] == 'bot':
        return build_bot_response(intent_request)
        
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.

    """
    intent_name = intent_request['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'Goodbye':
        return goodbye(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')

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
    
    intent_request = {'name': event['currentIntent']['name'], 'confirmationStatus': event['currentIntent']['confirmationStatus'], 'type': 'bot'}
    
    return dispatch(intent_request)
    