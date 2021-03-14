#!/usr/bin/env python

import requests
import json
import sys
from pathlib import Path
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pprint import pprint
import pandas as pd
import  re
from datetime import datetime

here = Path(__file__).parent.absolute()
repository_root = (here / ".." ).resolve()
sys.path.insert(0, str(repository_root))

import env

inv_url = env.UMBRELLA.get("inv_url")
inv_token = env.UMBRELLA.get("inv_token")
en_url = env.UMBRELLA.get("en_url")
en_key = env.UMBRELLA.get("en_key")

# enter here the domains
domains = ["internetbadguys.com"]

inv_headers = {
    "Accept": "application/json",
    "Authorization": f'Bearer {inv_token}'}

en_headers = {
    'Content-type': 'application/json', 
    'Accept': 'application/json'
    }

for domain in domains:
    #Construct the API request to the Umbrella Investigate API to query for the status of the domain
    url = f"{inv_url}/domains/categorization/{domain}?showLabels"
    response = requests.get(url, headers=inv_headers)
    response.raise_for_status()

    domain_status = response.json()[domain]["status"]

    print("Domain status for domain" + re.sub("(?<=[a-z])\.(?=[a-z])", "(dot)", domain) + ":\n")
    pprint(response.json()[domain], indent=4)

    # get domain historical information
    url = f"{inv_url}/pdns/name/{domain}"
    querystring = {"sortorder": "desc"}

    response = requests.get(url, headers=inv_headers, params=querystring)
    response.raise_for_status()

    domain_records = pd.DataFrame(response.json()["records"])
    domain_records['name'] = domain_records.apply(lambda x: re.sub("(?<=[a-z])\.(?=[a-z])", "(dot)", x['name']), axis=1)
    print(domain_records)

    if domain_status == 1:
        print(f"The domain {domain} is found CLEAN")
    elif domain_status == -1:
        print(f"The domain {domain} is found MALICIOUS")
        
        # add malicious domain to a block list
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.0Z")

        url = f"{en_url}/events?customerKey={en_key}"

        payload = {
            "alertTime": now,
            "deviceId": "ba6a59f4-e692-4724-ba36-c28132c761de",
            "deviceVersion": "13.7a",
            "dstDomain": domain,
            "dstUrl": "http://" + domain + "/",
            "eventTime": now,
            "protocolVersion": "1.0a",
            "providerName": "Security Platform"
        }

        response = requests.post(url, headers=en_headers, data=json.dumps(payload))
        response.raise_for_status()

    elif domain_status == 0:
        print(f"The domain {domain} is found UNDEFINED")




