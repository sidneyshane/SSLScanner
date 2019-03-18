#   Author: Sidney Shane Dizon
#   Copyright (c) 2019 Sidney Shane Dizon
#   Program: getsslreport.py
#       Python Module for the Qualys SSL Labs Server Test that return a grading
#       for atleast one endpoint for a given website domain. This start a new request
#       every time and not from cache.


import requests
import time

API = 'https://api.ssllabs.com/api/v2/'
SERVER = "www.westjet.com" #Can be changed to a desired website domain


# This is a helper method that takes the path to the relevant API call and the
# user-defined payload and requests the data/server test from Qualys SSL labs.
# RETURNS JSON formatted data
def requestAPI(path, payload={}):
    url = API + path
    try:
        response = requests.get(url, params=payload)
    except requests.exception.RequestException:
        logging.exception('Request failed.')
        sys.exit(1)
    data = response.json()
    return data

#This starts a NEW SCAN to retrieve data. This does not retrieve data from the cache.
def newScan(host, publish='off', startNew='on', all='done', ignoreMismatch='on'):
    path = 'analyze'
    payload = {
                'host': host,
                'publish': publish,
                'startNew': startNew,
                'all': all,
                'ignoreMismatch': ignoreMismatch
              }
    results = requestAPI(path, payload)
    payload.pop('startNew')
    while results['status'] != 'READY' and results['status'] != 'ERROR':
        print("Scan still in progress") # Indicator of progress
        time.sleep(10) # Wait for response from API
        results = requestAPI(path, payload)

    return results


# Initiate scan
data = newScan(SERVER)
# Print result in terminal
print(SERVER, "'s SSL grade is:", data['endpoints'][0]['grade'])
