import requests
from requests.auth import HTTPBasicAuth
from env import config

# Connect to Meraki API
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": config['MERAKI_KEY']
}

orgs_url = f"{config['MERAKI_BASE_URL']}/organizations"


try: 
    response = requests.get(orgs_url, headers=headers)

    if response.status_code == 200:
        responses = response.json() 
        for res in responses:
            print("Id:" + str(res['id']) + ", Name: " + str(res['name']))

except Exception as ex:
    print(ex)