import requests
import json
import urllib

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

def get_playlist(playlist_id):
    access_token = get_access_token()
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    r = requests.get(BASE_URL + 'playlists/' + playlist_id + '/tracks', headers=headers)

    return r.json()


def get_tracks_from_playlist(playlist_id):
    playlist = get_playlist(playlist_id)

    


# --- test here --- 
FLOWERS_ID = '0yLdNVWF3Srea0uzk55zFn'
BILLBOARD_ID = '6UeSakyzhiEt4NB3UAd6NQ'
print(get_playlist(BILLBOARD_ID))