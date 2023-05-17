# This file will be dedicated to get songs detail from a playlist then get all the ID's of the song

#%% Import Library
from configparser import ConfigParser
import requests
import json
import re

#%% Get Token

parser = ConfigParser()
_ = parser.read('notebook.cfg')

# Retrieve the Credentials
client_id, client_secret = parser.get('app_test', 'client_id'), parser.get('app_test', 'client_secret')

url = "https://accounts.spotify.com/api/token"

payload=f'client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': '__Host-device_id=AQA1E_8u1HHZzuE7O9d_fV4YwanfNozg6q_mdfweHpowhpZGWG9saI45tX6W5no4APxdKSdgb0ZqexZNfHeYiXVZhLhlP5JYj0M; sp_tr=false'
}

response = requests.request("POST", url, headers=headers, data=payload)

AccessToken = json.loads(response.text)['access_token']

#%% Get ID from the playlist
## What are the song characteristics you want to extract? Everything.

### INPUT PLAYLIST ID HERE ###
link = 'https://open.spotify.com/playlist/37i9dQZF1E36tDNad90Y3t?si=d6cbf006bb604238'

playlist_id = re.search(r'(?<=playlist/)\w+', link).group()


# Playlist Detail
url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

payload={}
headers = {
  'Authorization': f'Bearer {AccessToken}'
}

playlistDetails = requests.get(url, headers=headers, data=payload).json()

print(f"Playlist Name: {playlistDetails['name']}")

#%% Get Tracks from the playlist

import requests

url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

payload={}
headers = {
  'Authorization': f'Bearer {AccessToken}'
}

response = requests.get(url, headers=headers, data=payload).json()

id_list = []
id_list = [song['track']['id'] for song in response['items']]

#%% Get Artists' ID from the song

artist_list = []
for _ in id_list:
    url = f"https://api.spotify.com/v1/tracks/{_}"

    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {AccessToken}'
    }

    response = requests.get(url, headers=headers, data=payload).json()

    artist_list.append(response['artists'][0]['id'])


#%% Get artist Genre

for artist in artist_list: 
    url = f'https://api.spotify.com/v1/artists/{artist}'

    payload = {}
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {AccessToken}'
    }

    response = requests.get(url, headers=headers, data=payload).json()

    print(response['name'], response['genres'])
