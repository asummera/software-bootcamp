import requests
from requests.auth import HTTPBasicAuth
from env import config
import json

# Meraki access
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": config['MERAKI_KEY']
}

orgs_url = f"{config['MERAKI_BASE_URL']}/organizations"
orgId = None

try: 
    response = requests.get(orgs_url, headers=headers)

    if response.status_code == 200:
        organizations = response.json() 
        for org in organizations:
            if org['name'] == 'DevNet Sandbox':
                orgId = org['id']

except Exception as ex:
    print(ex)


networks_url = f"{config['MERAKI_BASE_URL']}/organizations/{orgId}/networks"
networkId = None

try: 
    response = requests.get(networks_url, headers=headers)

    if response.status_code == 200:
        networks = response.json() 
        for network in networks:
            if network['name'] == 'DevNet Sandbox ALWAYS ON':
                networkId = network['id']

except Exception as ex:
    print(ex)

devices_url = f"{config['MERAKI_BASE_URL']}/networks/{networkId}/devices"
inventory = []

try: 
    response = requests.get(devices_url, headers=headers)

    if response.status_code == 200:
        devices = response.json() 
        for device in devices:
            inventory.append({
                'name' : device['name'],
                'type' : device['model'],
                'mac address' : device['mac'],
                'serial' : device['serial'],
                'category': 'Meraki'
                }) 

except Exception as ex:
    print(ex)


# DNAC access #
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
dnac_auth_url = f"{config['DNAC_BASE_URL']}/dna/system/api/v1/auth/token"

try:
    response = requests.post(dnac_auth_url, headers=headers, auth=HTTPBasicAuth(config['DNAC_USER'], config['DNAC_PASSWORD']))
    
    if response.status_code == 200:
        headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-auth-token": response.json()['Token']
        }   

except Exception as ex:
    print(ex)

dnac_devices_url = f"{config['DNAC_BASE_URL']}/dna/intent/api/v1/network-device"

try:
    response = requests.get(dnac_devices_url, headers=headers)
    
    if response.status_code == 200:
        devices = response.json()['response']
        for device in devices:
            inventory.append({
                    'name' : device['hostname'],
                    'type' : device['type'],
                    'mac address' : device['macAddress'],
                    'serial' : device['serialNumber'],
                    'category': 'DNA Center'
                    }) 

except Exception as ex:
    print(ex)

with open('stage2.json', 'w') as fp:
    json.dump(inventory, fp, indent=4)