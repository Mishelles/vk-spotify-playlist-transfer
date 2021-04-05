import requests
import time
import yaml
import re
from nltk.tokenize import RegexpTokenizer
from get_root_access_token_for_sp import get_token


class SpotifyUtil:

    def __init__(self):
        self._prepare_config()
        self._revoke_user_token()
        self._revoke_root_token()

    def _prepare_config(self) -> None:
        with open('creds.yaml', 'r') as c:
            self._config = yaml.safe_load(c)

    def _revoke_root_token(self):
        self._config['sp_root_token'] = get_token()

    def _revoke_user_token(self):
        response = requests.post(url='https://accounts.spotify.com/api/token',
                                 data={
                                     'refresh_token': self._config.get("sp_refresh_token"),
                                     'grant_type': 'refresh_token'
                                 },
                                 headers={
                                     "Authorization": 'Basic {}'.format(self._config.get('sp_basic_auth'))
                                 }).json()
        self._config['sp_access_token'] = response['access_token']

    def batch_track_search(self, track_list) -> list:
        track_list_spotify = []
        for song in track_list:
            title = song['title']
            artist = song['artist']
            cleaned_title = self.__class__._clean(title)
            cleaned_artist = self.__class__._clean(artist)
            try:
                track_id, track_name = self.search_track_on_spotify(cleaned_title + " " + cleaned_artist)
            except Exception:
                try:
                    track_id, track_name = self.search_track_on_spotify(cleaned_title)
                except Exception as ex:
                    print(cleaned_title + " " + cleaned_artist + ' not found!  ' + ex.__str__())
                else:
                    track_list_spotify.append({'Track name': track_name, 'id': track_id})
            else:
                track_list_spotify.append({'Track name': track_name, 'id': track_id})
            time.sleep(0.2)

        return track_list_spotify

    def create_playlist_in_spotify(self, level=0) -> str:
        if level > 2:
            raise SpotifyAuthException
        result = requests.post(
            url='https://api.spotify.com/v1/users/{}/playlists'.format(self._config.get('sp_user_id')),
            json={
                "name": self._config.get("sp_playlist_name"),
                "description": self._config.get("sp_playlist_description"),
                "public": self._config.get("sp_is_playlist_public")
            },
            headers={
                "Authorization": 'Bearer {}'.format(self._config.get('sp_access_token'))
            }
        )
        if result.status_code == 401:
            self._revoke_user_token()
            return self.create_playlist_in_spotify(level + 1)
        try:
            playlist_id = result.json()['id']
        except Exception:
            raise SpotifySearchException

        return playlist_id

    def search_track_on_spotify(self, query, level=0) -> (str, str):
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
            self._revoke_root_token()
            return self.search_track_on_spotify(query, level + 1)
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

    def add_tracks_to_playlist(self, tracks, id, level=0) -> None:
        if level > 2:
            raise SpotifyAuthException
        tracks_str = ','.join(tracks)
        res = requests.post(
            url='https://api.spotify.com/v1/playlists/{}/tracks?uris={}'.format(id, tracks_str),
            headers={
                "Authorization": 'Bearer {}'.format(self._config.get('sp_access_token'))
            }
        )
        if res.status_code == 401:
            self._revoke_user_token()
            return self.add_tracks_to_playlist(tracks, id, level + 1)

    @staticmethod
    def _clean(clean_sting) -> str:
        clean_sting = re.sub(r'([^)]*)\W', '', clean_sting)
        clean_sting = re.sub(r'\[[^)]*]\W', '', clean_sting)
        clean_sting = re.sub(r'(?i)(\s*)f(?:ea)?t(?:(?:\.?|\s)|uring)(?=\s).*$', '', clean_sting)
        clean_sting = re.sub(r'(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d', '', clean_sting)
        if re.match(r'\s*[^0-9]+\s*', clean_sting):
            clean_sting = re.sub(r'[0-9]+', '', clean_sting)
        tokenizer = RegexpTokenizer(r'\w+')
        return " ".join(tokenizer.tokenize(clean_sting))


class SpotifyException(Exception):
    def __str__(self):
        return self.__class__.__name__


class SpotifySearchException(SpotifyException):
    pass


class SpotifyAuthException(SpotifyException):
    pass
