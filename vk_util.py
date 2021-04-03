from vkaudiotoken import get_vk_official_token
import requests
import json
import time
import yaml


with open('creds.yaml', 'r') as c:
    config = yaml.safe_load(c)

creds_from_vk = get_vk_official_token(config.get('vk_login'), config.get('vk_password'))
config['vk_token'] = creds_from_vk['token']
config['vk_user_agent'] = creds_from_vk['user_agent']

sess = requests.session()
sess.headers.update({'User-Agent': config.get('vk_user_agent')})

page_size = 200
total_tracks = sess.get(
    "https://api.vk.com/method/audio.get",
    params=[('access_token', config.get('vk_token')),
            ('v', config.get('vk_version'))]
).json()['response']['count']

i = 0
all_tracks = []

while i < total_tracks - page_size:
    current_page_tracks = sess.get(
        "https://api.vk.com/method/audio.get",
        params=[('access_token', config.get('vk_token')),
                ('v', config.get('vk_version')),
                ('count', page_size),
                ('offset', i)]
    ).json()['response']['items']
    all_tracks += [{'artist': l['artist'], 'title': l['title']} for l in current_page_tracks]
    i += page_size
    time.sleep(1)

mod = total_tracks % page_size
current_page_tracks = sess.get(
        "https://api.vk.com/method/audio.get",
        params=[('access_token', config.get('vk_token')),
                ('v', config.get('vk_version')),
                ('count', mod),
                ('offset', i)]
    ).json()['response']['items']
all_tracks += [{'artist': l['artist'], 'title': l['title']} for l in current_page_tracks]
time.sleep(1)

with open('tracksFromVk.json', 'w', encoding='utf-8') as s:
    s.write(json.dumps(all_tracks, indent=2, ensure_ascii=False))
