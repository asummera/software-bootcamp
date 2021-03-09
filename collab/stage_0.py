import requests

from env import config

s = requests.Session()
s.headers.update({
    'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"
})

# Verify api access
WEBEX_BASE_URL = config['WEBEX_BASE_URL']

url = f"{WEBEX_BASE_URL}/v1/rooms"
id = None

resp = s.get(url)

if resp.status_code == 200:
    rooms = resp.json()['items']
    for room in rooms:
        if room['title'] == 'CSAP Programmability CTF - Team 2':
            id = room['id']

print(id)

