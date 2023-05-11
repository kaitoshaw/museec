# Library
import pandas as pd
import requests
import json
from creds import getCreds

# Loading data into Dataframe
filename = 'dataset/partial.csv'
df = pd.read_csv(filename)

# Retrieve the Credentials
client_id, client_secret = getCreds()

# Basic Song Retrieving Functions
def getToken(client_id, client_secret):
    # Get token
    url = "https://accounts.spotify.com/api/token"

    payload=f'client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '__Host-device_id=AQA1E_8u1HHZzuE7O9d_fV4YwanfNozg6q_mdfweHpowhpZGWG9saI45tX6W5no4APxdKSdgb0ZqexZNfHeYiXVZhLhlP5JYj0M; sp_tr=false'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    AccessToken = json.loads(response.text)['access_token']
    return AccessToken

# Access Token Retrieval
accessToken = getToken(client_id, client_secret)

def getAudioFeature(AccessToken, song_id):
    url = f"https://api.spotify.com/v1/audio-features/{song_id}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {AccessToken}'
    }

    songAudioFeature = requests.get(url, headers=headers, data=payload).json()

    return songAudioFeature

# Song's Audio Feature
def querySong(song_id):
    songQueue = getAudioFeature(accessToken, song_id)
    querySong = [songQueue['danceability'],
            songQueue['energy'],
            songQueue['loudness'],
            songQueue['mode'],
            songQueue['speechiness'],
            songQueue['acousticness'],
            songQueue['instrumentalness'],
            songQueue['liveness'],
            songQueue['valence']]
    return querySong

print(querySong('4AElkruOc9gECdltSuV3JN'))