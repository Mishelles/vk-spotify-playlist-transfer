import os
import uuid

import yaml

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

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
    login: str
    password: str


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
    print(response)
    try:
        redis_client.mset({
            dto.session_id: {
                'spotify': {
                    'sp_access_token': response['access_token'],
                    'sp_refresh_token': response['refresh_token']
                }
            }
        })
    except KeyError:
        raise HTTPException(status_code=400, detail='Invalid code provided')


@app.post("/login/vk", status_code=200)
def login_to_vk(dto: VkLoginInputDto):
    pass
