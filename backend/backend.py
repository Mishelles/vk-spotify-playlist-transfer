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

import redis

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


redis_client = redis.Redis()

with open('creds.yaml', 'r') as c:
    config = yaml.safe_load(c)

SPOTIFY_REDIRECT_URL = os.environ.get('SPOTIFY_REDIRECT_URL', 'http://localhost:3000/spotify-callback')

class BaseInputDto(BaseModel):
    session_id: str

class SpotifyLoginInputDto(BaseInputDto):
    code: str

class VkLoginInputDto(BaseInputDto):
    vkLogin: str
    vkPass: str

class InitSessionResponseDto(BaseModel):
    session_id: str


def generate_session_id():
    return uuid.uuid4()

# TODO how would it be connected to the UI?
@app.post("/init-session", status_code=200)
def init_session() -> InitSessionResponseDto:
    session_id = generate_session_id()
    if redis_client.get(session_id):
        redis_client.delete(session_id)
    return InitSessionResponseDto(session_id=session_id)


@app.post("/login/spotify", status_code=200)
def login_to_spotify(dto: SpotifyLoginInputDto):
    print("Code " + dto.code)
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
        redis_client.mset({
            dto.session_id: json.dumps({
                'spotify': {
                    'sp_access_token': response['access_token'],
                    'sp_refresh_token': response['refresh_token']
                }
            })
        })
    except KeyError:
        raise HTTPException(status_code=400, detail='Invalid code provided')


@app.post("/login/vk", status_code=200)
def login_to_vk(dto: VkLoginInputDto) -> VkLoginInputDto:
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
    access_token = credentials_from_vk['access_token']
    print("VK token: " + access_token)
    session = requests.session()
    session.headers.update({'User-Agent': supported_clients.VK_OFFICIAL.user_agent})
    try:
        redis_client.mset({
            dto.session_id: json.dumps({
                'vk': {
                    'vk_session': json.dumps(dict(session)),
                    'access_token': access_token
                }
            })
        })
    except KeyError:
        raise HTTPException(status_code=400, detail='Invalid code provided')
    return VkLoginInputDto