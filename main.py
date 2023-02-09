import requests
import json
import urllib

SPOTIFY_BASE_URI = 'https://api.spotify.com/v1'
CLIENT_ID = 'REDACTED_SPOTIFY_CLIENT_ID'

def get_access_code():
    REDIRECT_URI = 'http://localhost:8888/callback'
    response = requests.get(
        'https://accounts.spotify.com/authorize',
        params = {
            'client_id': urllib.parse.quote(CLIENT_ID.encode("utf-8")),
            'response_type': 'token',
            'redirect_uri': urllib.parse.quote(REDIRECT_URI.encode("utf-8"))
        }
    )
    # str_enc.decode('utf8', 'strict')
    # response_text = response.text.decode('utf8', 'strict')

    # json_data = json.loads(response_text)
    return response.text

# https://developer.spotify.com/documentation/web-api/reference/#/operations/get-track
# https://developer.spotify.com/console/get-track/ 
# GET /tracks/{id}
# def get_track(track_id):
#     response = requests.get(
#         SPOTIFY_BASE_URI + f'/tracks/{track_id}',
#         headers = {
#             "Authorization": f"Bearer {ACCESS_TOKEN}",
#             "market": "GB"
#         }
#     }
#     json_resp = response.json()
#     return json_resp

# --- test here --- 

# FLOWERS_ID = '0yLdNVWF3Srea0uzk55zFn'
# print(get_track(FLOWERS_ID))

print(get_access_code())