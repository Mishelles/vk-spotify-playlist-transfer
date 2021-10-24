import os
import uuid
import json

import yaml

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from vkaudiotoken import (
    TokenReceiverOfficial,
    CommonParams,
    TokenException,
    TwoFAHelper,
    supported_clients
)

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


with open('creds.yaml', 'r') as c:
    config = yaml.safe_load(c)

SPOTIFY_REDIRECT_URL = os.environ.get('SPOTIFY_REDIRECT_URL', 'http://localhost:3000/spotify-callback')
VK_API_DEFAULT_VERSION = '5.95'

sp_code = ''
sp_access_token = ''
sp_refresh_token = ''
sp_playlist_id =''

vk_session = None
vk_access_token = ''

last_iteration = False
batch = 0
offset = 0
page_size=200

class SpotifyLoginInputDto(BaseModel):
    code: str

class VkLoginInputDto(BaseModel):
    vkLogin: str
    vkPass: str

def generate_session_id():
    return uuid.uuid4()

@app.post("/login/spotify", status_code=200)
def login_to_spotify(dto: SpotifyLoginInputDto):
    print("Code " + dto.code)
    global sp_code
    sp_code = dto.code
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
        global sp_access_token
        sp_access_token = response['access_token']
        global sp_refresh_token
        sp_refresh_token = response['refresh_token']
    except KeyError:
        raise HTTPException(status_code=400, detail='Invalid code provided')


@app.post("/login/vk", status_code=200)
def login_to_vk(dto: VkLoginInputDto):
    print("Login: " + dto.vkLogin + ", pass: " + dto.vkPass)
    params = CommonParams(supported_clients.VK_OFFICIAL.user_agent)
    receiver = TokenReceiverOfficial(dto.vkLogin, dto.vkPass, params)
    try:
        credentials_from_vk = receiver.get_token()
    except TokenException as err:
        if err.code == TokenException.TWOFA_REQ and 'validation_sid' in err.extra:
           TwoFAHelper(params).validate_phone(err.extra['validation_sid'])
           print('2FA auth enabled. SMS should be sent')
           """ auth_code = input('Please, wait for SMS and insert your authorization code below: \n')
           receiver = TokenReceiverOfficial(self._config.get('vk_login'), self._config.get('vk_password'), params, auth_code)
           try:
               credentials_from_vk = receiver.get_token()
           except Exception as e:
               raise """
        else:
            raise
    token = credentials_from_vk['access_token']
    print("VK token: " + token)
    session = requests.session()
    session.headers.update({'User-Agent': supported_clients.VK_OFFICIAL.user_agent})
    try:
        global vk_session
        vk_session = session
        global vk_access_token
        vk_access_token = token
    except KeyError:
        raise HTTPException(status_code=400, detail='Invalid code provided')


@app.post("/init-transfer", status_code=200)
def init_process():
    print("Process has started")
    vk_total_tracks = get_total_tracks()
    print("VK total tracks: ")
    print(vk_total_tracks)
    global sp_playlist_id
    sp_playlist_id = create_playlist_in_spotify()
    print("SP playlist id: " + sp_playlist_id)
    for batch in self:
        print("yee")
#         tracks = spotify_util.batch_track_search(batch)
#         spotify_util.add_tracks_to_playlist([track['id'] for track in tracks], playlist_id)

def get_total_tracks() -> int:
    return vk_session.get(
        url="https://api.vk.com/method/audio.get",
        params=[
            ('access_token', vk_access_token),
            ('v', config.get('vk_version', VK_API_DEFAULT_VERSION))
        ]
    ).json()['response']['count']


def revoke_user_token(self):
    response = requests.post(
        url='https://accounts.spotify.com/api/token',
        data={
            'refresh_token': sp_refresh_token,
            'grant_type': 'refresh_token'
        },
        headers={
            "Authorization": 'Basic {}'.format(sp_code)
        }
    ).json()
    global sp_access_token
    sp_access_token = response['access_token']


def create_playlist_in_spotify(level=0) -> str:
    if level > 2:
        raise SpotifyAuthException
    result = requests.post(
        url='https://api.spotify.com/v1/users/{}/playlists'.format(config.get('sp_user_id')),
        json={
            "name": config.get("sp_playlist_name"),
            "description": config.get("sp_playlist_description"),
            "public": config.get("sp_is_playlist_public")
        },
        headers={
            "Authorization": 'Bearer {}'.format(sp_access_token)
        }
    )
    if result.status_code == 401:
        revoke_user_token()
        return create_playlist_in_spotify(level + 1)
    try:
        playlist_id = result.json()['id']
    except Exception:
        raise SpotifySearchException
    return playlist_id


def __iter__(self):
        return self


def __next__(self):
    if last_iteration:
        raise StopIteration
    if offset < total_tracks - page_size:
        page_size = page_size
    else:
        page_size = total_tracks % page_size
        last_iteration = True
    current_page_tracks = vk_session.get(
        url="https://api.vk.com/method/audio.get",
        params=[
            ('access_token', vk_access_token),
            ('v', config.get('vk_version', VK_API_DEFAULT_VERSION)),
            ('count', page_size),
            ('offset', offset)
        ])
    current_page_tracks = current_page_tracks.json()['response']['items']
    offset += page_size
    return [{'artist': l['artist'], 'title': l['title']} for l in current_page_tracks]


class SpotifyException(Exception):
    def __str__(self):
        return self.__class__.__name__


class SpotifySearchException(SpotifyException):
    pass


class SpotifyAuthException(SpotifyException):
    pass

