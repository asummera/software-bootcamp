import requests
import json
from pprint import pprint
import csv
import pandas as pd
from datetime import datetime

from utils.auth import IntersightAuth, get_authenticated_aci_session
from env import config


aci_session = get_authenticated_aci_session(config['ACI_USER'], config['ACI_PASSWORD'], config['ACI_BASE_URL'])

if aci_session is not None:
    print("ACI access verified")
else:
    print("Failed to verify access to ACI.")

# get the overall system health
base_url = config['ACI_BASE_URL']
url= f"{base_url}/api/class/fabricHealthTotal.json"

response = aci_session.get(url)
dateTimeObj = datetime.now()

if response.status_code == 200:
    print("Intersight access verified")
else:
    print(f"Intersight access denied. status code: {response.status_code}")

# for each fabric read out info (contains the main fabric and pod-1) 
out = []
for fabric in response.json()['imdata']:
    temp = fabric['fabricHealthTotal']['attributes']

    out.append({
        'healthScore': temp['cur'], 
        'maxSeverity': temp['maxSev'],
        'dn': temp['dn'],
        'timestamp': dateTimeObj
    })

pd.DataFrame(out).to_csv('stage-2.csv')

