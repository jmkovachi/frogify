import base64
import json

import requests

__all__ = ['SpotifyWrapper']

# TODO: Make this not a magic string. Generate with Django.
REDIRECT_URI = 'http://localhost:8000/frogify/redirect_login'

# TODO: These are fine.
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
ENDPOINT_FMT = 'https://api.spotify.com/v1/{}'


# TODO: Function only ever used once ever. Consider making it not a function.
# TODO: DRY - Don't Repeat Yourself.
# TODO: Consider moving reading Client-ID and Client Secret to `settings.py`
def get_id_and_secret():
    """
    Reads client id and secret from a file on the local file system.
    """
    try:
        with open('secret', 'r') as file:
            text = file.read()
        return text.split('\n')
    except:
        print('cannot find file with id and secret')
        return '', ''


# TODO: Avoid globals
CLIENT_ID, CLIENT_SECRET = get_id_and_secret()


class SpotifyWrapper:

    def __init__(self, client_id=None, client_secret=None):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.auth_header = 'TODO'  # TODO

    def get_access_token(self, auth_code):
        print('code ' + auth_code)
        code_payload = {
            "grant_type": "authorization_code",
            "code": str(auth_code),
            "redirect_uri": REDIRECT_URI
        }
        data_str = "{}:{}".format(self.client_id, self.client_secret)

        b64_auth_str = base64.urlsafe_b64encode(data_str.encode()).decode()

        headers = {"Authorization": "Basic {}".format(b64_auth_str)}
        post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

        response_data = json.loads(post_request.text)

        #print(response_data)

        access_token = response_data["access_token"]
        refresh_token = response_data["refresh_token"]
        token_type = response_data["token_type"]
        expires_in = response_data["expires_in"]

        return access_token

    def start_playback(self, uris=None):
        requests.put('https://api.spotify.com/v1/me/player/play', data=json.dumps({'uris': uris}),
                     headers=self.auth_header)

    def get_playlist_tracks(self, href=None):
        playlist_endpoint = '{}/tracks'.format(href)
        return json.loads(requests.get(playlist_endpoint, headers=self.auth_header).text)['items']

    def get_user_playlists(self, username=None, headers=None):
        playlists = requests.get('https://api.spotify.com/v1/users/{}/playlists'.format(username),
                                 headers=headers)
        return playlists.json()['items']
