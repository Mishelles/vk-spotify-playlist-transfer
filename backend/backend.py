import os

import yaml

import requests
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

app = FastAPI()

with open('creds.yaml', 'r') as c:
    config = yaml.safe_load(c)

SPOTIFY_REDIRECT_URL = os.environ.get('SPOTIFY_REDIRECT_URL', 'http://localhost:3000/spotify-callback')


class SpotifyLoginDto(BaseModel):
    code: str


@app.post("/login/spotify", status_code=200)
def login_to_spotify(dto: SpotifyLoginDto):
    response = requests.post(
        url='https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'authorization_code',
            'code': dto.code,
            'redirect_uri': SPOTIFY_REDIRECT_URL
        },
        headers={
            "Authorization": 'Basic {}'.format(config.get('sp_basic_auth'))
        }).json()
    try:
        config['sp_access_token'] = response['access_token']
        config['sp_refresh_token'] = response['refresh_token']
    except KeyError:
        raise HTTPException(status_code=400, detail='Invalid code provided')
    else:
        with open('creds.yaml', 'w') as file_object:
            yaml.safe_dump(config, file_object)
