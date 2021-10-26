import os
import uuid
import json

import yaml
import re
from nltk.tokenize import RegexpTokenizer

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from get_root_access_token_for_sp import get_token

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
vk_total_tracks = 0

last_iteration = False
batch = 0
offset = 0
page_size=200

class SpotifyLoginInputDto(BaseModel):
    code: str

class VkLoginInputDto(BaseModel):
    vkLogin: str
    vkPass: strt

class BatchSizeDto(BaseModel):
    size: str


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
    global vk_total_tracks
    vk_total_tracks = get_total_tracks()
    print("VK total tracks: ")
    print(vk_total_tracks)
    global sp_playlist_id
    sp_playlist_id = create_playlist_in_spotify()
    print("SP playlist id: " + sp_playlist_id)


@app.get('/get-batch', status_code=200)
def process_batch(dto: BatchSizeDto):
    print("yee " + dto.size)
    batch = getTracksFromVK(dto.size)
    print(batch)
    tracks = batch_track_search(batch)
    add_tracks_to_playlist([track['id'] for track in tracks], sp_playlist_id)


def get_total_tracks() -> int:
    return vk_session.get(
        url="https://api.vk.com/method/audio.get",
        params=[
            ('access_token', vk_access_token),
            ('v', config.get('vk_version', VK_API_DEFAULT_VERSION))
        ]
    ).json()['response']['count']


def _revoke_root_token():
    config['sp_root_token'] = get_token()


def revoke_user_token():
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
        raise Exception
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
        raise Exception
    return playlist_id


def getTracksFromVK(offset):
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


def batch_track_search(track_list) -> list:
    track_list_spotify = []
    for song in track_list:
        title = song['title']
        artist = song['artist']
        cleaned_title = clean(title)
        cleaned_artist = clean(artist)
        try:
            track_id, track_name = search_track_on_spotify(cleaned_title + " " + cleaned_artist)
        except Exception:
            try:
                track_id, track_name = search_track_on_spotify(cleaned_title)
            except Exception as ex:
                print(cleaned_title + " " + cleaned_artist + ' not found!  ' + ex.__str__())
            else:
                track_list_spotify.append({'Track name': track_name, 'id': track_id})
        else:
            track_list_spotify.append({'Track name': track_name, 'id': track_id})
        time.sleep(0.2)

    return track_list_spotify


def search_track_on_spotify(query, level=0) -> (str, str):
    if level > 2:
        raise SpotifyAuthException
    response = requests.get(
        url='https://spclient.wg.spotify.com/searchview/km/v4/search/{}'.format(query),
        params={
            'catalogue': '',
            'country': 'RU'
        },
        headers={
            'Authorization': "Bearer {}".format(self._config.get('sp_root_token')),
            'Host': "spclient.wg.spotify.com"
        }
    )
    if response.status_code == 401:
        revoke_root_token()
        return search_track_on_spotify(query, level + 1)
    elif response.status_code == 404:
        raise Exception
    else:
        try:
            results = response.json()
        except Exception:
            raise Exception

        try:
            track_id = results['results']['tracks']['hits'][0]['uri']
            track_returned_name = results['results']['tracks']['hits'][0]['name']
        except Exception:
            raise Exception

        return track_id, track_returned_name


def add_tracks_to_playlist(tracks, id, level=0) -> None:
    if level > 2:
        raise Exception
    tracks_str = ','.join(tracks)
    res = requests.post(
        url='https://api.spotify.com/v1/playlists/{}/tracks?uris={}'.format(id, tracks_str),
        headers={
            "Authorization": 'Bearer {}'.format(self._config.get('sp_access_token'))
        }
    )
    if res.status_code == 401:
        revoke_user_token()
        return add_tracks_to_playlist(tracks, id, level + 1)


@staticmethod
def clean(clean_sting) -> str:
    # Remove "()"
    clean_sting = re.sub(r'\([^)]*\)', '', clean_sting)
    # Remove "[]"
    clean_sting = re.sub(r'\[[^)]*\]', '', clean_sting)
    # Remove "feat."
    clean_sting = re.sub(r'(?i)(\s*)f(?:ea)?t(?:(?:\.?|\s)|uring)(?=\s).*$', '', clean_sting)
    # Remove date
    clean_sting = re.sub(r'(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d', '', clean_sting)
    # Remove numbers
    if re.match(r'\s*[^0-9]+\s*', clean_sting):
        clean_sting = re.sub(r'[0-9]+', '', clean_sting)
    # Remove other garbage
    tokenizer = RegexpTokenizer(r'\w+')
    return " ".join(tokenizer.tokenize(clean_sting))