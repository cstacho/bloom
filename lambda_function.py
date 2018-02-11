import get_opps
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

    
def volunteer(intent_request):
    result = get_opps.get_opportunities()
    if intent_request['sessionAttributes'] and intent_request['currentIntent']['confirmationStatus'] == 'Confirmed':
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                     "contentType": "PlainText",
                     "content": "Thank you! We've signed you up for " + intent_request['sessionAttributes']['opp'] + " on " + intent_request['currentIntent']['slots']['DayOfWeek'] + ". Thank you for helping women bloom!"
                },
            }
        }
    else:
        return { "dialogAction": {
            "type": "ConfirmIntent",
            "message": {
                 "contentType": "PlainText",
                 "content": "How about volunteering with " + result["name"] +"?" + " " + result["description"]
             },
             "intentName": "Volunteer",
             "slots": intent_request['currentIntent']['slots']
             ,
             }
             ,
             "sessionAttributes": { 
                "opp": result["name"]
                }
            }

    
    
    

def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'Volunteer':
        return volunteer(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')




def lambda_handler(event, context):
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    print(event)
    return dispatch(event)
