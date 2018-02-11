import json

import requests
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from . import spotify as spw


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

# Redirect URI and scopes used for our application
REDIRECT_URI = 'http://localhost:8000/frogify/redirect_login'
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SCOPE = ('playlist-modify-public playlist-modify-private '
         'user-read-currently-playing user-modify-playback-state '
         'user-read-private playlist-read-private playlist-modify-public '
         'playlist-modify-private ugc-image-upload user-top-read '
         'user-read-recently-played')

# Base url and version number
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Auth query parameters for getting auth token
auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}


def index(request):
    """
    Index route
    """
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'frogify/index.html')


def login(request):
    """
    Login route. Redirects to a spotify authentication url.
    """
    url = "&".join(["{}={}".format(key, val) for key, val in auth_query_parameters.items()])

    auth_url = "{}/?{}".format("https://accounts.spotify.com/authorize", url)
    return redirect(auth_url)


def redirect_login(request):
    request.session['auth_code'] = request.GET['code']

    auth_code = request.session['auth_code']

    wrapper = spw.SpotifyWrapper()

    request.session['access_token'] = wrapper.get_access_token(auth_code)

    return redirect('/frogify/queue')


def queue(request):
    """
    Redirect uri used upon login. Source: https://github.com/drshrey/spotify-flask-auth-example/blob/master/main.py
    """
    print(request.session.keys())
    access_token = request.session['access_token']


    """access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]"""

    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    wrapper = spw.SpotifyWrapper()

    # sp = spotipy.Spotify(auth=access_token)
    # playlists = sp.user_playlists('jmkovachi')
    playlists = wrapper.get_user_playlists(username='jmkovachi', headers=authorization_header)
    # playlist_id = playlists['items'][10]['id']
    playlist_items = []
    for item in playlists:
        playlist_items.append({
            'href': item['href'],
            'name': item['name'],
        })

    #return render(request, 'frogify/event.html',)
    return render(request, 'frogify/event.html', {'playlists' : playlist_items})

    #return HttpResponse('Response received')



def createRoom(request):
    """
    Creates room using playlist id.
    """
    playlist = request.POST['playlist']

    playlist_endpoint = '{}/tracks'.format(SPOTIFY_API_URL)

    playlist_response = requests.get(playlist_endpoint, headers=authorization_header)

    
