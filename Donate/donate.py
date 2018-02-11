import logging
import time
import os
import requests 
import json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
customerId = '5a7f998e5eaa612c093b0e69'
apiKey='5bf049de46c6d16eebbdbce2076aeb95'
payeeId = '5a7f998e5eaa612c093b0e6a'

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

    
def donate(intent_request):
    
    payload = {
        "medium": "balance",
        "payee_id": "5a7f998e5eaa612c093b0e6a",
        "description": "string",
        "amount": intent_request['currentIntent']['slots']['Amount'].replace("$","")
    }
    response = requests.post( 
        url, 
        data=json.dumps(payload),
        headers={'content-type':'application/json'},)

    if response.status_code == 200:
     print('transfer created')
    
    return { "dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
        "message": {
             "contentType": "PlainText",
             "content": "You're an awesome human being for donating to " + intent_request['currentIntent']['slots']['Org']
         }
        }
    }

def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'Donation':
        return donate(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')




def lambda_handler(event, context):
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    print(event)
    return dispatch(event)
