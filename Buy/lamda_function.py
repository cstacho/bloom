import get_bizz
import logging
import time
import os
import random
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }
    
def build_bot_response(intent_request):
    result = get_bizz.get_bizz()
    cool = get_bizz.cool()
    if intent_request['sessionAttributes'] and intent_request['confirmationStatus'] == 'Confirmed':
        bizz_result = intent_request['sessionAttributes']['opp']
        company= random.choice(list(get_bizz.bizz[intent_request['sessionAttributes']['opp']]))
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                     "contentType": "PlainText",
                     "content": "Did you know about the " + cool + " " + bizz_result + " company " + company + " ? " + get_bizz.bizz[bizz_result][company]
                },
            }
        }
    else:
        return { 
            "dialogAction": {
                "type": "ConfirmIntent",
                "message": {
                     "contentType": "PlainText",
                     "content": "Would you like to discover a women owned " + result + " business?"
                 },
                 "intentName": "Buy",
                 
                 }
                 ,
                 "sessionAttributes": { 
                    "opp": result
                    }
            }
    
def discover(intent_request):
    if intent_request['type'] == 'bot':
        return build_bot_response(intent_request)
    else:
        return build_alexa_response(intent_request)
    
    
    

def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    """
    intent_name = intent_request['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'Buy':
        return discover(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')




def lambda_handler(event, context):
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    print(event)
    if 'currentIntent' in event:
        intent_request = {'name': event['currentIntent']['name'], 'sessionAttributes': event['sessionAttributes'], 'confirmationStatus': event['currentIntent']['confirmationStatus'], 'type': 'bot'}
    else:
        intent_request = {'name': event['request']['intent']['name'],'sessionAttributes': event['session']['attributes'], 'type': 'echo'}
    return dispatch(intent_request)
