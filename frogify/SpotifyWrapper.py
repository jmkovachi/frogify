import requests
import json
import base64
import urllib

REDIRECT_URI = 'http://localhost:8000/frogify/redirect_login'
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

def get_id_and_secret():
    """
    Reads client id and secret from a file on the local file system.
    """
    try:
        with open('secret', 'r') as file:
            text = file.read()
            client_id = text.split('\n')[0]
            client_secret = text.split('\n')[1]
            print(client_id)
            return client_id, client_secret
    except Exception as e:
        print('cannot find file with id and secret')
        return '', ''


CLIENT_ID, CLIENT_SECRET = get_id_and_secret()


class SpotifyWrapper:

    @staticmethod
    def get_access_token(auth_code):
        print('code ' + auth_code)
        code_payload = {
            "grant_type": "authorization_code",
            "code": str(auth_code),
            "redirect_uri": REDIRECT_URI
        }
        data_str = "{}:{}".format(CLIENT_ID, CLIENT_SECRET)

        b64_auth_str = base64.urlsafe_b64encode(data_str.encode()).decode()

        headers = {"Authorization": "Basic {}".format(b64_auth_str)}
        post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

        response_data = json.loads(post_request.text)

        print(response_data)

        access_token = response_data["access_token"]
        refresh_token = response_data["refresh_token"]
        token_type = response_data["token_type"]
        expires_in = response_data["expires_in"]

        return access_token

    @staticmethod
    def start_playback(uris=[], auth_header={}):
        requests.put('https://api.spotify.com/v1/me/player/play', data=json.dumps({'uris' : uris}), headers=auth_header)

    @staticmethod
    def get_playlist_tracks(href='', auth_header={}):
        playlist_endpoint = '{}/tracks'.format(href)
        return json.loads(requests.get(playlist_endpoint, headers=auth_header).text)['items']

    @staticmethod
    def get_user_playlists(username='', auth_header={}):
        playlists = requests.get('https://api.spotify.com/v1/users/{}/playlists'.format(username), headers=auth_header).text
        print(playlists)
        return json.loads(playlists)['items']
