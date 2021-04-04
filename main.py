from vkaudiotoken import get_vk_official_token
import requests
import json
import time
import yaml
import requests
import json
import time
import yaml
import re
from nltk.tokenize import RegexpTokenizer
import spotify_util as spotify
import vk_util as vk

'''
    Execute steps:
        1. Get VK token
        2. Get Spotify root token
        3. Create playlist at Spotify
        4. Get first 200 tracks from VK
        5. Find 200 tracks at Spotify
        6. Add 200 tracks to playlist
        7. Repeat steps 4-6 till we get all tracks.
'''

vk_session = vk.prepare_vk_session()

