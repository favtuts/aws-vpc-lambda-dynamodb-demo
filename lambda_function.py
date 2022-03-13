import os
import logging
import boto3
import json
import random
import string

from pythonjsonlogger import jsonlogger

# Setup logging
DEFAULT_LOGLEVEL = 'DEBUG'
LOGGER = logging.getLogger()
LOGGER.setLevel(DEFAULT_LOGLEVEL)
HANDLER = logging.StreamHandler()
HANDLER.setFormatter(jsonlogger.JsonFormatter())
LOGGER.handlers.clear()
LOGGER.addHandler(HANDLER)

# minimize boto logging
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

RESPONSE_HEADERS = {
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with,x-id-token,x-refresh-token,x-last-login',
        'Access-Control-Allow-Methods': 'OPTIONS, POST',
        'Access-Control-Allow-Origin': '*',
        'Allow': 'OPTIONS, POST',
        'Content-Type': 'application/json'
}


# set up clients and resources
ddbclient = boto3.client('dynamodb')

# load environment variables
tablename = os.environ.get('TableName', None)
keyname = os.environ.get('KeyName', None)


def build_success_response(payload=None):
    '''
    Send Success
    Send a successful web request with payload
    '''
    status_code = 200

    response = {
        'headers': RESPONSE_HEADERS,
        'statusCode': status_code,
    }

    details = {
        'response': response,
        'payload': payload
    }
    LOGGER.debug('building success response', extra=details)
    if payload is not None:
        response['body'] = json.dumps(payload)

    return response

def build_fail_response(status_code):
    '''
    Send Fail Response
    Send a failed web request
    '''
    response = {
        'headers': RESPONSE_HEADERS,
        'statusCode': status_code,
    }

    return response


def dynamodb_add_data(tablename, keyname, stringdata):
    response = ddbclient.put_item(
        Item={
            keyname: {
                'S': stringdata
            }
        },
        ReturnConsumedCapacity='TOTAL',
        TableName=tablename
    )
    return (response)

def lambda_handler(event, context):
    '''
    Lambda Entrypoint
    '''    
    LOGGER.debug('processing event', extra={'event': event})

    # response_payload
    payload = {}
    try:
        if tablename is None:
            raise Exception('expected to find dynamodb tablename at environment variable TableName, found nothing')
        if keyname is None:
            raise Exception('expected to find dynamodb keyname at environment variable KeyName, found nothing')

        # Generate a random string to ensure no duplicates are put into DDB table
        randomstring = (''.join(random.choice(string.ascii_letters) for i in range(10)))
        LOGGER.info('random string generated: %s', randomstring)

        details = {
            'random_string': randomstring            
        }
        payload["random_string"] = randomstring

        # Store the generated string into Dynamodb table
        LOGGER.info('saving random string ...')        
        ddb_response = dynamodb_add_data(tablename, keyname, randomstring)
        LOGGER.info('saved with response', extra=ddb_response)
        payload["saved_response"] = ddb_response

        LOGGER.info('event is processed successfully', extra=details)
        return build_success_response(payload)
    except Exception:        
        LOGGER.exception('Unable to process request',exc_info=True)
        return build_fail_response(status_code=500)
