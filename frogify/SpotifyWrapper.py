import requests

REDIRECT_URI = 'http://localhost:8000/frogify/queue'

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


def SpotifyWrapper():


	@staticmethod
	def get_access_token(auth_code):
		code_payload = {
	        "grant_type": "authorization_code",
	        "code": str(auth_code),
	        "redirect_uri": REDIRECT_URI
    	}

	@staticmethod
	def start_playback(uris=[], auth_header={}):
		requests.put('https://api.spotify.com/v1/me/player/play', data=json.dumps({'uris' : uris}), headers=auth_header)

	@staticmethod
	def get_playlist_tracks(href='', auth_header={}):
		playlist_endpoint = '{}/tracks'.format(href)
		return json.loads(requests.get(playlist_endpoint, headers=auth_header).text)['items']

	@staticmethod
	def get_user_playlists(username='', auth_header={}):
		return json.loads(requests.get('https://api.spotify.com/v1/users/{}/playlists'.format(username), headers=auth_header).text)['items']
