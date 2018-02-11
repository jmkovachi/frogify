import json

import requests

# TODO: Make this not a magic string. Generate with Django.
REDIRECT_URI = 'http://localhost:8000/frogify/queue'


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


CLIENT_ID, CLIENT_SECRET = get_id_and_secret()


class SpotifyWrapper:
    ENDPOINT_FMT = 'https://api.spotify.com/v1/{}'

    def __init__(self, client_id=None, client_secret=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_header = 'TODO'  # TODO

    def get_access_token(self, auth_code):
        code_payload = {
            "grant_type": "authorization_code",
            "code": str(auth_code),
            "redirect_uri": REDIRECT_URI
        }

    def start_playback(self, uris=None):
        requests.put(self.ENDPOINT_FMT.format('/me/player/play'), data=json.dumps({'uris': uris}),
                     headers=self.auth_header)

    def get_playlist_tracks(self, href=None):
        playlist_endpoint = '{}/tracks'.format(href)
        return json.loads(requests.get(playlist_endpoint, headers=self.auth_header).text)['items']

    def get_user_playlists(self, username=None):
        response = requests.get(self.ENDPOINT_FMT.format('/users/{}/playlists').format(username),
                                headers=self.auth_header)
        return response.json()['items']
