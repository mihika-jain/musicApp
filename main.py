import requests
import pprint
import json
import urllib
import database
from datetime import datetime
from database import *

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

CLIENT_ID = 'REDACTED_SPOTIFY_CLIENT_ID'
CLIENT_SECRET = 'REDACTED_SPOTIFY_CLIENT_SECRET'

# ----------------------------------------------------------------------

def get_access_token():
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    return auth_response_data['access_token']

# ----------------------------------------------------------------------

def get_track(track_id):
    access_token = get_access_token()
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

    return r.json()

# ----------------------------------------------------------------------

def get_playlist_tracks(playlist_id):
    access_token = get_access_token()
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    r = requests.get(BASE_URL + 'playlists/' + playlist_id + '/tracks', headers=headers)

    json_data = r.json()

    # write JSON data to file
    with open('playlist_data.json', 'w') as out_file:
        json.dump(json_data, out_file, ensure_ascii=False)


# ----------------------------------------------------------------------

def playlist_tracks_to_database(file_name):
    # convert file to dictionary
    with open(file_name) as in_file:
        playlist_dict = json.load(in_file)

    # pprint.pprint(playlist_dict)
    # loop thru dictionary get track IDs and store track data into DB
    count = 1.0
    for track in playlist_dict['items']:
        # pprint.pprint(track)
        track_id = track['track']['id']
        track_info = get_track(track_id)
        # print(track_info)
        database.insert_track(track_info, count)
        count += 1

# ----------------------------------------------------------------------

# --- test here --- 
FLOWERS_ID = '0yLdNVWF3Srea0uzk55zFn'
BILLBOARD_ID = '6UeSakyzhiEt4NB3UAd6NQ'
# print(get_playlist_tracks(BILLBOARD_ID))

# playlist_tracks_to_dict('playlist_data.json')

playlist_tracks_to_database('playlist_data.json')