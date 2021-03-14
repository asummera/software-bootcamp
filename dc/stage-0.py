import requests
import json
from pprint import pprint

from utils.auth import IntersightAuth
from env import config

auth=IntersightAuth(secret_key_filename=config['INTERSIGHT_CERT'],
                      api_key_id=config['INTERSIGHT_API_KEY'])
BASE_URL='https://www.intersight.com/api/v1'


url = f"{BASE_URL}/ntp/Policies"
response = requests.get(url, auth=auth)


if response.status_code == 200:
    print("Intersight access verified")
else:
    print(f"Intersight access denied. status code: {response.status_code}")


pprint('Print the ntp Policies:')
pprint('------------------------')
pprint(response.json()['Results'], indent=4)






