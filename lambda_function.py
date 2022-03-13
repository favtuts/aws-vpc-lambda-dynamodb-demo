import os
import logging
import boto3
import json

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

def lambda_handler(event, context):
    '''
    Lambda Entrypoint
    '''    
    LOGGER.debug('processing event', extra={'event': event})

     # response_payload
    payload = {}
    try:
        details = {
            'hello': 'Hello My Function'            
        }
        payload["response"] = "Hi, Warmly welcome"

        LOGGER.info('event is processed successfully', extra=details)
        return build_success_response(payload)
    except Exception:
        details = {'payload': payload}
        LOGGER.exception('Unable to process request', extra=details)
        return build_fail_response(status_code=500)
