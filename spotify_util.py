import requests
import json
import time
import yaml
import re
from nltk.tokenize import RegexpTokenizer
from get_root_access_token_for_sp import get_token

with open('creds.yaml', 'r') as c:
    config = yaml.safe_load(c)


class SpotifyException(Exception):
    def __str__(self):
        return self.__class__.__name__


class SpotifySearchException(SpotifyException):
    pass


class SpotifyAuthException(SpotifyException):
    pass


def clean(t, a):
    without_brackets = re.sub(r'\([^)]*\)\W', '', t + " " + a)
    without_feat = re.sub(r'(?i)(\s*)f(?:ea)?t(?:(?:\.?|\s)|uring)(?=\s)', '', without_brackets)
    tokenizer = RegexpTokenizer(r'\w+')
    return " ".join(tokenizer.tokenize(without_feat))


def revoke_root_token():
    config['sp_root_token'] = get_token()


def search_track_on_spotify(query, level=0):
    if level > 2:
        raise SpotifyAuthException
    response = requests.get(
        'https://spclient.wg.spotify.com/searchview/km/v4/search/{}'.format(query),
        params={
            'catalogue': '',
            'country': 'RU'
        },
        headers={
            'Authorization': "Bearer {}".format(config.get('sp_root_token')),
            'Host': "spclient.wg.spotify.com"
        }
    )
    if response.status_code == 401:
        revoke_root_token()
        return search_track_on_spotify(query, level + 1)
    elif response.status_code == 404:
        raise SpotifySearchException
    else:
        try:
            results = response.json()
        except Exception:
            raise SpotifySearchException

        try:
            track_id = results['results']['tracks']['hits'][0]['uri']
            track_returned_name = results['results']['tracks']['hits'][0]['name']
        except Exception:
            raise SpotifySearchException

        return track_id, track_returned_name


def add_tracks_to_playlist(tracks, id, level=0):
    if level > 2:
        raise SpotifyAuthException
    tracks_str = ','.join(tracks)
    res = requests.post(
        'https://api.spotify.com/v1/playlists/{}/tracks?uris={}'.format(id, tracks_str),
        headers={
            "Authorization": 'Bearer {}'.format(config.get('sp_access_token'))
        }
    )
    if res.status_code == 401:
        revoke_user_token()
        return add_tracks_to_playlist(tracks, id, level + 1)


def create_playlist_in_spotify(level=0):
    if level > 2:
        raise SpotifyAuthException
    result = requests.post(
        'https://api.spotify.com/v1/users/{}/playlists'.format(config.get('sp_user_id')),
        json={
            "name": "Test playlist",
            "description": "New playlist description",
            "public": 'false'
        },
        headers={
            "Authorization": 'Bearer {}'.format(config.get('sp_access_token'))
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


def revoke_user_token():
    response = requests.post('https://accounts.spotify.com/api/token',
                             data={'refresh_token': config.get("sp_refresh_token"), 'grant_type': 'refresh_token'},
                             headers={"Authorization": 'Basic {}'.format(config.get('sp_basic_auth'))}).json()
    config['sp_access_token'] = response['access_token']


with open('tracksFromVk.json', 'r') as s:
    track_list_vk = json.load(s)

track_list_spotify = []


for song in track_list_vk:
    title = song['title']
    artist = song['artist']
    clear_query_string = clean(title, artist)
    try:
        track_id, track_name = search_track_on_spotify(clear_query_string)
    except Exception as e:
        print(clear_query_string + ' not found!  ' + e.__str__())
    time.sleep(0.2)

with open('spotifyIds.json', 'w', encoding='utf-8') as s:
    s.write(json.dumps(track_list_spotify, indent=2, ensure_ascii=False))

with open('spotifyIds.json', 'r') as s:
    track_list_spotify = json.load(s)

sp_playlist_id = create_playlist_in_spotify()

ids_to_insert = []
i = 0
for t in track_list_spotify:
    i += 1
    ids_to_insert.append(t['id'])
    if i == 10:
        i = 0
        add_tracks_to_playlist(ids_to_insert, sp_playlist_id)
        ids_to_insert = []
