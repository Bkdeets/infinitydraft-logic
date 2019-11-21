import decimal
import boto3
import json
import os
import soc

def has_allowed_params(params):
    allowed_params = {
        'number_of_teams', 
        'file',
        'budget',
        'gameType'
    }
    if params:
        return allowed_params >= params.keys()
    else:
        return True

def lambda_handler(event, context):
    query_parameters = event['params']
    sport = query_parameters.get('sport')

    sport_functions = {
        "SOC": soc.main
    }

    if not(has_allowed_params(query_parameters)):
        return api_response(400, {"Message": "Incorrect query string specified"})
    
    try:
        body = resource_functions[sport](query_parameters)
    except Exception as e:
        return api_response(500, {"Message": "There was a problem handling this request"})

    print(api_response(200, body))

    return api_response(200, body)