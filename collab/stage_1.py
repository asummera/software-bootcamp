import requests

from env import config

s = requests.Session()
s.headers.update({
    'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"
})

WEBEX_BASE_URL = config['WEBEX_BASE_URL']

url = f"{WEBEX_BASE_URL}/v1/rooms"
payload = {
    'title': 'My Local Test Space'
}
roomId = None
 
resp = s.post(url, data=payload)

if resp.status_code == 200:
    roomId = resp.json()['id']
    with open("env.py", "a") as fo:
        fo.write(f"\nconfig['TESTING_ROOM'] = \"{roomId}\"") 

#roomId = config['TESTING_ROOM']

url = f"{WEBEX_BASE_URL}/v1/memberships"
add_to_space = ['mneiding@cisco.com', 'frewagne@cisco.com']

for cec in add_to_space:
    payload = {
        'roomId': roomId,
        'personEmail': cec
        }
    resp = s.post(url, data=payload)

url = f"{WEBEX_BASE_URL}/v1/messages"
payload = {
    'roomId': roomId,
    'text': 'Hi! Danke für den Kurs heute, hat echt Spass gemacht :)'.encode('latin-1')
    }
resp = s.post(url, data=payload)
