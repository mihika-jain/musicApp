import os
import requests
import pprint
import json
import urllib
import database
from datetime import datetime
from database import *

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# Spotify API credentials are read from environment variables (see .env.example)
CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']

# ----------------------------------------------------------------------

def get_access_token():
    '''
        uses ids from spotify developer account to retrieve an access token for spotify database 
        returns: access token (string)
    '''
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
    '''
        Given track ID (str), accesses Spotify database and 
        returns:track info (dict)
    '''
    access_token = get_access_token()
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

    return r.json()

# ----------------------------------------------------------------------

def playlist_tracks_to_file(playlist_id, file_name):
    '''
        Given playlist id (str), accesses Spotify database and
        writes playlist info (dict) to playlist_data.json 
        returns: void
    '''
    access_token = get_access_token()
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    r = requests.get(BASE_URL + 'playlists/' + playlist_id + '/tracks', headers=headers)

    # write JSON data to file
    json_data = r.json()
    with open(file_name, 'w') as out_file:
        json.dump(json_data, out_file, ensure_ascii=False)


# ----------------------------------------------------------------------

def update_collection(playlist_id, file_name):
    '''
        given a playlist ID
        update the collection database to be accurate to the current playlist
        
    '''

    # update playlist json file
    playlist_tracks_to_file(playlist_id, 'playlist_data.json')

    # convert file to dictionary
    with open(file_name) as in_file:
        playlist_dict = json.load(in_file)

    # for all current documents in the database, set update parameter to 0
    db = database.get_database()
    collection = db['top100']
    database.update_many(collection)
    
    # iterate through updated file and add to / change all tracks 
    
    count = 1
    for track in playlist_dict['items']:
        track_id = track['track']['id']
        if(database.contains(collection, track_id)!= None):
            # update place to count make update 1
            database.find_one_and_update(collection, track_id, count)
        else:
            track_info = get_track(track_id)
            database.insert_track(collection, track_info, count)
        count+=1
    
    # iterate back through collection and remove all items that haven't been updated 
    database.delete_not_updated(collection)

# ----------------------------------------------------------------------


    
# ----------------------------------------------------------------------

FLOWERS_ID = '0yLdNVWF3Srea0uzk55zFn'
BILLBOARD_ID = '6UeSakyzhiEt4NB3UAd6NQ'
NEWPLAY_ID = '6dwkKfocksoZ6gtQYOTC2e'
FILENAME = 'playlist_data.json'

# database.delete_whole_collection()
update_collection(NEWPLAY_ID,FILENAME)