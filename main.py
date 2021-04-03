from vkaudiotoken import get_kate_token, get_vk_official_token
import vk
import requests
import json
import time
import yaml
import logging

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

with open('creds.yaml', 'r') as c:
    config = yaml.safe_load(c)


# print(get_vk_official_token(login, password))


def add_tracks_to_playlist(tracks, id):
    tracks_str = ','.join(tracks)
    res = requests.post(
        'https://api.spotify.com/v1/playlists/{}/tracks?uris={}'.format(id, tracks_str),
        headers={
            "Authorization": 'Bearer {}'.format(config.get('sp_access_token'))
        }
    ).json()


def create_playlist_in_spotify():
    playlist_id = requests.post(
        'https://api.spotify.com/v1/users/{}/playlists'.format(config.get('sp_user_id')),
        json={
            "name": "New Playlist",
            "description": "New playlist description",
            "public": 'false'
        },
        headers={
            "Authorization": 'Bearer {}'.format(config.get('sp_access_token'))
        }
    ).json()['id']
    return playlist_id


def perform_request_to_spotify(url, query):
    results = requests.get(url, params=query, headers={
        'Authorization': "Bearer {}".format(config.get('sp_access_token')),
        'Host': "spclient.wg.spotify.com"
    })

    if results.status_code == 401:
        config['sp_access_token'] = revoke_token(config.get('sp_refresh_token'))
        return perform_request_to_spotify(url, query)
    return results


def revoke_token(refresh_token: str):
    response = requests.post('https://accounts.spotify.com/api/token',
                             data={'refresh_token': refresh_token, 'grant_type': 'refresh_token'},
                             headers={"Authorization": 'Basic {}'.format(config.get('sp_basic_auth'))}).json()
    return response['access_token']


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

BASIC_QUERY_SP = 'https://spclient.wg.spotify.com/searchview/km/v4/search/{}'

# for song in track_list_vk:
#     title = song['title']
#     artist = song['artist']
#     query = BASIC_QUERY_SP.format(artist + " " + title)
#     response = perform_request_to_spotify(query, {
#         'catalogue': '',
#         'country': 'RU'
#     })
#
#     if response.status_code == 404:
#         continue
#     response = response.json()
#
#     try:
#         track_id = response['results']['tracks']['hits'][0]['uri']
#         track_returned_name = response['results']['tracks']['hits'][0]['name']
#         track_list_spotify.append({'name': track_returned_name, 'id': track_id})
#     except IndexError:
#         print('title ' + title + ' artist ' + artist + ' not found! ')
#     except KeyError:
#         print('title ' + title + ' artist ' + artist + ' not found! (Key error)')
#     finally:
#         time.sleep(0.2)
#
# with open('spotifyIds.json', 'w', encoding='utf-8') as s:
#     s.write(json.dumps(track_list_spotify, indent=2, ensure_ascii=False))

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
