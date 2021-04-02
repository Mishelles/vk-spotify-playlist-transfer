from vkaudiotoken import get_kate_token, get_vk_official_token
import vk
import requests
import json
import time
import spotipy
import yaml

with open ('creds.yaml', 'r') as c:
    config = yaml.safe_load(c)

# print(get_vk_official_token(login, password))

sess = requests.session()
sess.headers.update({'User-Agent': config.get('user_agent')})

page_size = 100
total_tracks = sess.get(
    "https://api.vk.com/method/audio.get",
    params=[('access_token', config.get('vk_token')),
            ('v', config.get('version'))]
).json()['response']['count']

print(sess.get(
    "https://api.vk.com/method/audio.get",
    params=[('access_token', config.get('token')),
            ('v', config.get('version')),
            ('offset', 3900),
            ('count', 100)]
).json()['response']['items'])

i = 0
all_tracks = []
while i < total_tracks - page_size:
    current_page_tracks = sess.get(
        "https://api.vk.com/method/audio.get",
        params=[('access_token', config.get('vk_token')),
                ('v', config.get('version')),
                ('count', page_size),
                ('offset', i)]
    ).json()['response']['items']
    all_tracks += [{'artist': l['artist'], 'title': l['title']} for l in current_page_tracks]
    i += page_size
    print('Current page tracks: ' + str(i))
    time.sleep(1)

with open('tracksFromVk.json', 'w', encoding='utf-8') as s:
    s.write(json.dumps(all_tracks, indent=2, ensure_ascii=False))

sp = spotipy.Spotify(config.get('sp_token'))

with open('tracksFromVk.json', 'r') as s:
    track_list_vk = json.load(s)

track_list_spotify = []

for song in track_list_vk[:10]:
    title = song['title']
    results = sp.search(q=title, type='track')
    try:
        current_track_id = results['tracks']['items'][0]['id']
        track_list_spotify.append({'title: ': title, 'id: ': current_track_id})
        time.sleep(1)
    except IndexError:
        print('No tracks found for title: ' + title)

with open('spotifyIds.json', 'w', encoding='utf-8') as s:
    s.write(json.dumps(track_list_spotify, indent=2, ensure_ascii=False))

# 200 per page
