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
popularity = []
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

#%% Generate New Dataset

## THE CODE RUNNER SHOULD STARTS HERE
IDExtract = []
duplicates = []
def getSongFromPlaylist(playlist_url):

  playlist_id = re.search(r'(?<=playlist/)\w+', playlist_url).group()

  # Playlist Detail
  url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

  payload={}
  headers = {
    'Authorization': f'Bearer {AccessToken}'
  }

  response = requests.get(url, headers=headers, data=payload).json()
  # print(response['items'][0]['track']['popularity'])

  for j in response['items']:
    # print(j['items'][0]['track']['popularity'])
    print(len(j))

  # id_list = [song['track']['id'] for song in response['items']]
  # for _ in id_list:
  #   if _ not in IDExtract:
  #     if len(IDExtract) <= 1000:
  #       IDExtract.append(_)
  #     else:
  #       pass
  #   else:
  #     # Duplicates
  #     duplicates.append('0')

# getSongFromPlaylist('https://open.spotify.com/playlist/2usrWKLYxYdm3aqWThf7G9?si=47b7293a6fad4ca7')
#%%
getSongFromPlaylist('https://open.spotify.com/playlist/1X1zynBURpogqyLjnOEHB6?si=652bfc1d00684f0c')

# %% Run Several Playlists

origin = [
  # Spotify Top Hits
  'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=47c5db11a2984dae',
  'https://open.spotify.com/playlist/37i9dQZF1DWUa8ZRTfalHk?si=b4c1974e00cb4698',
  'https://open.spotify.com/playlist/37i9dQZF1DX2L0iB23Enbq?si=ba3ab09620f24252',
  'https://open.spotify.com/playlist/37i9dQZF1DXcRXFNfZr7Tp?si=2c26cc0fa6c949e0',
  'https://open.spotify.com/playlist/37i9dQZF1DXa2PvUpywmrr?si=406809633a9646a7',
  'https://open.spotify.com/playlist/37i9dQZF1DX0s5kDXi1oC5?si=0f938c49b3274f21',
  'https://open.spotify.com/playlist/37i9dQZF1DXbYM3nMM0oPk?si=00576616a64f47c2',
  'https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6?si=7d7fab35dca4474a',
  'https://open.spotify.com/playlist/37i9dQZF1DWUxHPh2rEiHr?si=0aead92c68d244cb',
  'https://open.spotify.com/playlist/37i9dQZF1DWUZMtnnlvJ9p?si=7c82ce34b989430f',
  # Daily Mix
  'https://open.spotify.com/playlist/37i9dQZF1E36tDNad90Y3t?si=95eade9c78fd48ba',
  'https://open.spotify.com/playlist/37i9dQZF1E38Hv1gtWXC9c?si=7e34affc1795445e',
  'https://open.spotify.com/playlist/37i9dQZF1E38VEJXRB5dXu?si=e9ebdd1909374670',
  'https://open.spotify.com/playlist/37i9dQZF1E3a6zdo1PRnea?si=bf902b07cca7427d',
  'https://open.spotify.com/playlist/37i9dQZF1E382LwL9sLLx3?si=eaeb6d8c016b4139',
  'https://open.spotify.com/playlist/37i9dQZF1E37qEfazBk7l0?si=4328794eaf3e4136'
]


### ACTUAL RUNNER ###

# Playlist List
for plist in origin:
  # Song in Playlist
  getSongFromPlaylist(plist)

IDExtract

#%% Get Audio Features
def getAudioFeatures(songID):
  # Playlist Detail
  url = f"https://api.spotify.com/v1/audio-features/{songID}"

  payload={}
  headers = {
    'Authorization': f'Bearer {AccessToken}'
  }

  response = requests.get(url, headers=headers, data=payload).json()
  return response

features = ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']


#%%
print(getAudioFeatures('47M43J3F3lCCI26YHUyOx8'))
# %%
print(f'Successfully Extracted {len(IDExtract)} songs, found {len(duplicates)} duplicates.')



#%%
### Runner V2.0

main_data = []
id_list = []

def getArtistGenre(artist_id):
  url_artistDetail = f'https://api.spotify.com/v1/artists/{artist_id}'

  payload = {}
  headers = {
    'Authorization': f'Bearer {AccessToken}'
  }

  genreFetch = requests.get(url_artistDetail, headers=headers, data=payload).json()
  return genreFetch['genres']
  
formatted = []

def getSongDatas(id):
  formatted = []

  url_audioFeature = f"https://api.spotify.com/v1/audio-features/{id}"
  url_trackFeature = f"https://api.spotify.com/v1/tracks/{id}"

  payload={}
  headers = {
    'Authorization': f'Bearer {AccessToken}'
  }
  track_feature = requests.get(url_trackFeature, headers=headers, data=payload).json()
  audio_features = requests.get(url_audioFeature, headers=headers, data=payload).json()

  # Get ID
  formatted.append(id)

  # Song Title
  formatted.append(track_feature['name'])

  # Artist List 
  temp_a = []
  temp_artist = [getArtistGenre(artist['id']) for artist in track_feature['artists']]
  for _i in temp_artist:
    for __i in _i:
      if __i in temp_a:
        pass
      else:
        temp_a.append(__i)

  formatted.append(temp_a)

  # Popularity
  formatted.append(track_feature['popularity'])

  # Audio Features
  for _ in audio_features:
    formatted.append(audio_features[_])

  return formatted

def playlistExtract(playlist_url):
  playlist_id = re.search(r'(?<=playlist/)\w+', playlist_url).group()

  url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

  payload={}
  headers = {
    'Authorization': f'Bearer {AccessToken}'
  }

  response = requests.get(url, headers=headers, data=payload).json()

  _data = [getSongDatas(song['track']['id']) for song in response['items']]

  for _singular in _data:
    main_data.append(_singular)

# origin = [
#   # Spotify Top Hits
#   'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=47c5db11a2984dae',
#   'https://open.spotify.com/playlist/37i9dQZF1DWUa8ZRTfalHk?si=b4c1974e00cb4698',
#   'https://open.spotify.com/playlist/37i9dQZF1DX2L0iB23Enbq?si=ba3ab09620f24252',
#   'https://open.spotify.com/playlist/37i9dQZF1DXcRXFNfZr7Tp?si=2c26cc0fa6c949e0',
#   'https://open.spotify.com/playlist/37i9dQZF1DXa2PvUpywmrr?si=406809633a9646a7',
#   'https://open.spotify.com/playlist/37i9dQZF1DX0s5kDXi1oC5?si=0f938c49b3274f21',
#   'https://open.spotify.com/playlist/37i9dQZF1DXbYM3nMM0oPk?si=00576616a64f47c2',
#   'https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6?si=7d7fab35dca4474a',
#   'https://open.spotify.com/playlist/37i9dQZF1DWUxHPh2rEiHr?si=0aead92c68d244cb',
#   'https://open.spotify.com/playlist/37i9dQZF1DWUZMtnnlvJ9p?si=7c82ce34b989430f',
#   # Daily Mix
#   'https://open.spotify.com/playlist/37i9dQZF1E36tDNad90Y3t?si=95eade9c78fd48ba',
#   'https://open.spotify.com/playlist/37i9dQZF1E38Hv1gtWXC9c?si=7e34affc1795445e',
#   'https://open.spotify.com/playlist/37i9dQZF1E38VEJXRB5dXu?si=e9ebdd1909374670',
#   'https://open.spotify.com/playlist/37i9dQZF1E3a6zdo1PRnea?si=bf902b07cca7427d',
#   'https://open.spotify.com/playlist/37i9dQZF1E382LwL9sLLx3?si=eaeb6d8c016b4139',
#   'https://open.spotify.com/playlist/37i9dQZF1E37qEfazBk7l0?si=4328794eaf3e4136'
# ]

origin = [
  # 'https://open.spotify.com/playlist/0ytnvx66xQwraz1WeAGtNm?si=7cdbfba2590c40d1',
  # 'https://open.spotify.com/playlist/0kgsupLF9ff61IvU005ZZX?si=156d749ce6b348f8',
  # 'https://open.spotify.com/playlist/0qLqTqVGRYf4QLrdBMfx68?si=4501a339ef1a434d',
  'https://open.spotify.com/playlist/15JzYvG16yNBeTgjQCORiO?si=14f63563cbce49d7'
]


for _playlist in origin:
  playlistExtract(_playlist)
  print(len(main_data))
#%%
print(main_data[0])
