#!/usr/bin/env python

import requests
import env
import pandas as pd 
from pprint import pprint
import json
import sys

amp_host = env.AMP.get("host")
amp_client_id = env.AMP.get("client_id")
amp_api_key = env.AMP.get("api_key")

amp_base_url = f"https://{amp_client_id}:{amp_api_key}@{amp_host}"
headers = {
    'Content-type': 'application/json', 
    'Accept': 'application/json'
    }

tg_sha = "b1380fd95bc5c0729738dcda2696aa0a7c6ee97a93d992931ce717a0df523967"

tg_host = env.THREATGRID.get("host")
tg_api_key = env.THREATGRID.get("api_key")

tg_base_url = f"https://{tg_host}/api/v2"


# get all event types from AMP
url = f"{amp_base_url}/v1/event_types"
response = requests.get(url, headers=headers)
response.raise_for_status()

event = list(filter(lambda x: x["name"]=="Executed malware", response.json()['data']))
eventType = event[0]['id']

# get the connector_guid
url = f"{amp_base_url}/v1/computers"
host = "Demo_AMP_Threat_Audit"
params = {
    "hostname[]": host,
}
response = requests.get(url, headers=headers, params=params)
response.raise_for_status()
connector_guid = response.json()['data'][0]['connector_guid']

# check executed malweare events that have occured on the host demo_amp_threat_audit
url = f"{amp_base_url}/v1/events"
params = {
    "event_type[]": eventType,
    "connector_guid[]": connector_guid
}
response = requests.get(url, headers=headers, params=params)
response.raise_for_status()

if len(response.json()['data'])>0:
    print('Results found:')
    for i in response.json()['data']:
        print('Event type: ' + str(i['event_type']) + '\n' + \
            'Event id: ' + str(i['event_type_id']) + '\n' + \
            'Connector guid: ' + str(i['connector_guid']) + '\n' + \
            'Hostname: ' + str(i['computer']['hostname'] + '\n'))
        
        pprint(response.json()['data'], indent=4)
        file_hash = i['file']['identity']['sha256']

        # isolate the host
        url = f"{amp_base_url}/v1/computers/{connector_guid}/isolation"
        try: 
            isolaiton_resp = requests.put(url, headers=headers)
            isolaiton_resp.raise_for_status()
        except requests.HTTPError as err:
            if isolaiton_resp.status_code == 409:
                print("The host is already isolated.")
            else:
                raise SystemExit(err)

        # Search for a submission in threadgrid
        url = f"{tg_base_url}/search/submissions?state=succ&q={tg_sha}&api_key={tg_api_key}"
        inv_response = requests.get(url, headers=headers)
        inv_response.raise_for_status()
        submissions = inv_response.json()['data']['items']

        submissions = list(filter(lambda x: x["item"]['sha256']==file_hash, inv_response.json()['data']['items']))
        if len(submissions) > 0:
            print('The sample has been submitted before!')
            sample = submissions[0]['item']['sample']
        
        else:
            print("File has not yet been submitted in ThreadGrid.")
            sys.exit()

        # Check for a domain that have been seen for the sample:
        url = f"{tg_base_url}/samples/feeds/domains?q={tg_sha}&api_key={tg_api_key}&sample={sample}"
        domains = requests.get(url, headers=headers)
        domains.raise_for_status()

        with open('stage-2.json', 'w') as out_file:
            json.dump(domains.json(), out_file, indent=4)
            
else:
    print('No results found.')
