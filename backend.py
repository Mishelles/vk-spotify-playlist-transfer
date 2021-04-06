import yaml

import requests

from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI()

with open('creds.yaml', 'r') as c:
    config = yaml.safe_load(c)

SPOTIFY_REDIRECT_URL = 'http://localhost:8000/spotify-login-callback'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize?client_id={}&response_type=code&redirect_uri={}&scope=playlist-modify-private'


@app.get("/spotify-login")
def spotify_uth():
    return RedirectResponse(url=SPOTIFY_AUTH_URL.format(config['sp_client_id'], SPOTIFY_REDIRECT_URL))


@app.get("/spotify-login-callback")
def spotify_login_callback(code: str):
    response = requests.post(
        url='https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': SPOTIFY_REDIRECT_URL
        },
        headers={
            "Authorization": 'Basic {}'.format(config.get('sp_basic_auth'))
        }).json()
    config['sp_access_token'] = response['access_token']
    config['sp_refresh_token'] = response['refresh_token']
    with open('creds.yaml', 'w') as c:
        yaml.safe_dump(config, c)
    return {
        'access_token': response['access_token'],
        'refresh_token': response['refresh_token']
    }
