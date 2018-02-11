import logging
import time
import os
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

        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled"
            }
        }
    
    
def volunteer(intent_request):
        return build_bot_response(intent_request)
    
    
    

def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    """
    intent_name = intent_request['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'Hello':
        return volunteer(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')




def lambda_handler(event, context):
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    print(event)
    if 'currentIntent' in event:
        intent_request = {'name': event['currentIntent']['name'], 'slots': event['currentIntent']['slots'], 'sessionAttributes': event['sessionAttributes'], 'confirmationStatus': event['currentIntent']['confirmationStatus'], 'type': 'bot'}
    else:
        intent_request = {'name': event['request']['intent']['name'], 'slots': event['request']['intent']['slots'], 'sessionAttributes': event['session']['attributes'], 'type': 'echo'}
    return dispatch(intent_request)
