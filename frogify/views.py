from django.http import HttpResponse
import urllib
from django.shortcuts import redirect
import requests
import base64
import json


def get_id_and_secret():
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

REDIRECT_URI = 'http://localhost:8000/frogify/queue'
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SCOPE = "playlist-modify-public playlist-modify-private"

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def login(request):
	url = "&".join(["{}={}".format(key, val) for key, val in auth_query_parameters.items()])

	auth_url = "{}/?{}".format("https://accounts.spotify.com/authorize", url)
	return redirect(auth_url)


def queue(request):
	auth_code = request.GET['code']

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

	return HttpResponse('You made it!')