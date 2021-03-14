#!/usr/bin/env python

import requests
import json
import sys
from pathlib import Path
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pprint import pprint
import pandas as pd

here = Path(__file__).parent.absolute()
repository_root = (here / ".." ).resolve()
sys.path.insert(0, str(repository_root))

import env

inv_url = env.UMBRELLA.get("inv_url")
inv_token = env.UMBRELLA.get("inv_token")
#Use a domain of your choice
domain = "exampleadultsite.com"

#Construct the API request to the Umbrella Investigate API to query for the status of the domain
url = f"{inv_url}/domains/categorization/{domain}?showLabels"
headers = {
    "Accept": "application/json",
    "Authorization": f'Bearer {inv_token}'}
response = requests.get(url, headers=headers)

#And don't forget to check for errors that may have occured!
response.raise_for_status()

#Make sure the right data in the correct format is chosen, you can use print statements to debug your code
domain_status = response.json()[domain]["status"]

if domain_status == 1:
    print(f"The domain {domain} is found CLEAN")
elif domain_status == -1:
    print(f"The domain {domain} is found MALICIOUS")
elif domain_status == 0:
    print(f"The domain {domain} is found UNDEFINED")

print("This is how the response data from Umbrella Investigate looks like: \n")
print(pd.DataFrame(response.json()))
print('\n')

#Add another call here, where you check the historical data for either the domain from the intro or your own domain and print it out in a readable format
domain = "internetbadguys.com"

url = f"{inv_url}/pdns/domain/{domain}"
querystring = {"sortorder":"desc"}
headers = {
    "Accept": "application/json",
    "Authorization": f'Bearer {inv_token}'}
response = requests.get(url, headers=headers, params=querystring)
response.raise_for_status()

domain_records = response.json()["records"]

print("This is the historical data for the domain " + domain + ", recrods are ordered in a descending order: \n")
print(pd.DataFrame(domain_records))
