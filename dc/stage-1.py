import requests
import json
import pandas as pd
from pprint import pprint

from utils.auth import IntersightAuth
from env import config

auth = IntersightAuth(secret_key_filename=config['INTERSIGHT_CERT'],
                      api_key_id=config['INTERSIGHT_API_KEY'])
BASE_URL = 'https://www.intersight.com/api/v1'

# Get all alarms
url = f"{BASE_URL}/cond/Alarms"
response = requests.get(url, auth=auth)

if response.status_code == 200:
    print("Intersight access verified")
else:
    print(f"Intersight access denied. status code: {response.status_code}")


desc = [{'Description': i["Description"]} for i in response.json()['Results']]

print('Description of all alarms:')
with pd.option_context('display.max_rows', None, 'display.max_colwidth', None):  
    print(pd.DataFrame(desc))
print('\n\n')


# Get a summary of the physical infrastructure
url = f"{BASE_URL}/compute/PhysicalSummaries"
response = requests.get(url, auth=auth)

if response.status_code == 200:
    print("Intersight access verified")
else:
    print(f"Intersight access denied. status code: {response.status_code}")

summaries = [{\
    'ManagementMode': i["ManagementMode"], \
    'MgmtIpAddress': i['MgmtIpAddress'], \
    'Name': i['Name'], \
    'CPUs': i['NumCpus'], \
    'Cores': i['NumCpuCores'], \
    'PowerState': i['OperPowerState'], \
    'Firmware': i['Firmware'], \
    'Model': i['Model'], \
    'Serial': i['Serial']\
    } for i in response.json()['Results']]

print('Summary of phyical infrastructure:\n')
print(pd.DataFrame(summaries))
print('\n\n')

# Get License infos
url = f"{BASE_URL}/license/LicenseInfos"
response = requests.get(url, auth=auth)

if response.status_code == 200:
    print("Intersight access verified")
else:
    print(f"Intersight access denied. status code: {response.status_code}")

licenses = [{ 'License': i["LicenseType"] } for i in response.json()['Results']]
print('The license tiers:\n')
print(pd.DataFrame(licenses))
print('\n\n')

# Get Compliance with Hardware Compatibility List (HCL)
url = f"{BASE_URL}/cond/HclStatuses"
response = requests.get(url, auth=auth)

if response.status_code == 200:
    print("Intersight access verified")
else:
    print(f"Intersight access denied. status code: {response.status_code}")

resp = [{'OsVendor': i['InvOsVendor'], 'OsVersion': i["InvOsVersion"], } for i in response.json()['Results']]
print('Os Vendor and Version:\n')
print(pd.DataFrame(resp))
print('\n\n')

# Get overview of all kubernetes clusters
url = f"{BASE_URL}/kubernetes/Clusters"
response = requests.get(url, auth=auth)

if response.status_code == 200:
    print("Intersight access verified")
else:
    print(f"Intersight access denied. status code: {response.status_code}")

resp = [{'Name': i["Name"]} for i in response.json()['Results']] 
print('Kubernetes clusters running on this cluster:\n')
print(pd.DataFrame(resp))
print('\n\n')

# Get all deployments running in the kubernetes cluster.
url = f"{BASE_URL}/kubernetes/Deployments"
response = requests.get(url, auth=auth)

if response.status_code == 200:
    print("Intersight access verified")
else:
    print(f"Intersight access denied. status code: {response.status_code}")

n_deployments = len(response.json()['Results'])
print('Number of deployments running in your kubernetes cluster is: ' + str(n_deployments))
