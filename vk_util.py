from vkaudiotoken import get_vk_official_token
import requests
import time
import yaml


class VkUtil:

    def __init__(self, page_size=200):
        self._batch = 0
        self._offset = 0
        self._prepare_config()
        self._page_size = page_size
        self._session = self._prepare_vk_session()
        self._total_tracks = self.get_total_tracks()
        self._last_iteration = False

    def _prepare_vk_session(self) -> requests.session:
        creds_from_vk = get_vk_official_token(self._config.get('vk_login'), self._config.get('vk_password'))
        self._config['vk_token'] = creds_from_vk['token']
        self._config['vk_user_agent'] = creds_from_vk['user_agent']
        sess = requests.session()
        sess.headers.update({'User-Agent': self._config.get('vk_user_agent')})
        return sess

    def _prepare_config(self) -> None:
        with open('creds.yaml', 'r') as c:
            self._config = yaml.safe_load(c)

    def get_total_tracks(self) -> int:
        return self._session.get(
            "https://api.vk.com/method/audio.get",
            params=[('access_token', self._config.get('vk_token')),
                    ('v', self._config.get('vk_version'))]
        ).json()['response']['count']

    def __iter__(self):
        return self

    def __next__(self):
        if self._last_iteration:
            raise StopIteration
        if self._offset < self._total_tracks - self._page_size:
            page_size = self._page_size
        else:
            page_size = self._total_tracks % self._page_size
            self._last_iteration = True
        current_page_tracks = self._session.get(
            "https://api.vk.com/method/audio.get",
            params=[('access_token', self._config.get('vk_token')),
                    ('v', self._config.get('vk_version')),
                    ('count', page_size),
                    ('offset', self._offset)]
        ).json()['response']['items']
        self._offset += page_size
        time.sleep(1)
        return [{'artist': l['artist'], 'title': l['title']} for l in current_page_tracks]
