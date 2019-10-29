#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import json

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = 'e86e027070cc4d328bdaef66cb6572b2'

def query_api(req):
    api = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = api.text_request()
    request.lang = 'en'
    request.session_id = req.get('session_id')
    request.query = req.get('query')
    response = request.getresponse()
    data = response.read()
    print(data)
    return data

def process_response(res):
    response = json.loads(res)
    result = response['result']
    action = result.get('action')

#    actionIncomplete = result.get('actionIncomplete', False)
 #   if action is not None:
  #      if action  == u"searchNearBy":
   #         if not actionIncomplete:
    #            parameters = result['parameters']
#
 #               category = parameters.get('category')
  #              address = parameters.get('address')
#
 #               print( "haha" + category + address)
#
 #           else:
  #              print(result['fulfillment'].get('speech'))
   #     if action == u"getInformation":
    #        if not actionIncomplete:
     #           parameters = result['parameters']
      #          company = parameters.get('company')
       #         print('Company ' + company)

def differentiateSearch(req):
    data = query_api(req)
    data = json.loads(data)
    result = data['result']
    metadata = result.get('metadata')
    if(metadata): 
        decision = metadata.get('intentName')
        return decision
    else:
        return 

def getConfirmation(req):
    data = query_api(req)
    data = json.loads(data)
    result = data['result']
    metadata = result.get('metadata')
    if(metadata.get('intentName') == u"Confirmation"):
        return result.get('parameters').get('Confirmation')
    return 
        
def trySearchCapability(req):
    data = query_api(req)
    data = json.loads(data)
    result = data['result']
    metadata = result.get('metadata')
    if(metadata.get('intentName') == u"SearchCapability"):
        return True
req = {}
req['session_id'] = '1234'
req['query'] = 'yay'
print(getConfirmation(req))

