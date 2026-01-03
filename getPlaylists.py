import requests
import os

BASE_URL = os.getenv('SPOTIFY_BASE_URL')
ACCESS_TOKEN = os.getenv('SPOTIFY_ACCESS_TOKEN')
LIMIT = 50
OFFSET = 0
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}
while True:
    response = requests.get(BASE_URL + 'me/tracks?limit=' + str(LIMIT) + '&offset=' + str(OFFSET), headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        OFFSET += LIMIT
    if not data['next']:
        break
