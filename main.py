from vkaudiotoken import get_kate_token, get_vk_official_token
import vk
import requests
import json
import time
import yaml
import logging
from .get_root_access_token_for_sp import get_token

# logging.basicConfig(level=logging.DEBUG)

'''
    Execute steps:
        1. Vk part (getting token, getting tracks from VK);
        2. Getting root token for Spotify
        3. Creating playlists in Spotify
        4. Adding tracks to Spotify

    TODO:
        1. Add regexp to clean track's name ('/' - is not valid)
            1.1 everything enclosed in brackets - \([^)]*\)\W
            1.2 everything non-word [^\w\s]
        2. Add proper mechanism for taking tokens
        
'''


class SpotifySearchException(Exception):
    pass


class SpotifyAuthException(Exception):
    pass


with open('creds.yaml', 'r') as c:
    config = yaml.safe_load(c)


# print(get_vk_official_token(login, password))

def tokenize(t, a):
    return t + " " + a


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
        add_tracks_to_playlist(tracks, id, level + 1)


def create_playlist_in_spotify(level=0):
    if level > 2:
        raise SpotifyAuthException
    result = requests.post(
        'https://api.spotify.com/v1/users/{}/playlists'.format(config.get('sp_user_id')),
        json={
            "name": "New Playlist",
            "description": "New playlist description",
            "public": 'false'
        },
        headers={
            "Authorization": 'Bearer {}'.format(config.get('sp_access_token'))
        }
    )
    if result.status_code == 401:
        revoke_user_token()
        create_playlist_in_spotify(level + 1)
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


# sess = requests.session()
# sess.headers.update({'User-Agent': config.get('user_agent')})
#
# page_size = 100
# total_tracks = sess.get(
#     "https://api.vk.com/method/audio.get",
#     params=[('access_token', config.get('vk_token')),
#             ('v', config.get('version'))]
# ).json()['response']['count']
#
# print(sess.get(
#     "https://api.vk.com/method/audio.get",
#     params=[('access_token', config.get('token')),
#             ('v', config.get('version')),
#             ('offset', 3900),
#             ('count', 100)]
# ).json()['response']['items'])
#
# i = 0
# all_tracks = []
# while i < total_tracks - page_size:
#     current_page_tracks = sess.get(
#         "https://api.vk.com/method/audio.get",
#         params=[('access_token', config.get('vk_token')),
#                 ('v', config.get('version')),
#                 ('count', page_size),
#                 ('offset', i)]
#     ).json()['response']['items']
#     all_tracks += [{'artist': l['artist'], 'title': l['title']} for l in current_page_tracks]
#     i += page_size
#     print('Current page tracks: ' + str(i))
#     time.sleep(1)
#
# with open('tracksFromVk.json', 'w', encoding='utf-8') as s:
#     s.write(json.dumps(all_tracks, indent=2, ensure_ascii=False))

with open('tracksFromVk.json', 'r') as s:
    track_list_vk = json.load(s)

track_list_spotify = []

for song in track_list_vk:
    title = song['title']
    artist = song['artist']
    clear_query_string = tokenize(title, artist)
    response = search_track_on_spotify(clear_query_string)

    if response.status_code == 404:
        continue
    response = response.json()

    try:
        track_id = response['results']['tracks']['hits'][0]['uri']
        track_returned_name = response['results']['tracks']['hits'][0]['name']
        track_list_spotify.append({'name': track_returned_name, 'id': track_id})
    except IndexError:
        print('title ' + title + ' artist ' + artist + ' not found! ')
    except KeyError:
        print('title ' + title + ' artist ' + artist + ' not found! (Key error)')
    finally:
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
