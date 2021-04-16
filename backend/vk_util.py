from vkaudiotoken import (
    TokenReceiverOfficial,
    CommonParams,
    TokenException,
    TwoFAHelper,
    supported_clients
)
import requests
import yaml

VK_API_DEFAULT_VERSION = '5.95'


class VkUtil:

    def __init__(self, page_size=200):
        self._batch = 0
        self._offset = 0
        self._access_token = None
        self._prepare_config()
        self._api_version = self._config.get('vk_version', VK_API_DEFAULT_VERSION)
        self._page_size = page_size
        self._session = self._prepare_vk_session()
        self._total_tracks = self.get_total_tracks()
        self._last_iteration = False

    def _prepare_vk_session(self) -> requests.session:
        params = CommonParams(supported_clients.VK_OFFICIAL.user_agent)
        receiver = TokenReceiverOfficial(self._config.get('vk_login'), self._config.get('vk_password'), params)
        try:
            credentials_from_vk = receiver.get_token()
        except TokenException as err:
            if err.code == TokenException.TWOFA_REQ and 'validation_sid' in err.extra:
                TwoFAHelper(params).validate_phone(err.extra['validation_sid'])
                print('2FA auth enabled. SMS should be sent')
                auth_code = input('Please, wait for SMS and insert your authorization code below: \n')
                receiver = TokenReceiverOfficial(self._config.get('vk_login'), self._config.get('vk_password'), params, auth_code)
                try:
                    credentials_from_vk = receiver.get_token()
                except Exception as e:
                    raise
            else:
                raise
        self._access_token = credentials_from_vk['access_token']
        sess = requests.session()
        sess.headers.update({'User-Agent': supported_clients.VK_OFFICIAL.user_agent})
        return sess

    def _prepare_config(self) -> None:
        with open('creds.yaml', 'r') as c:
            self._config = yaml.safe_load(c)

    def get_total_tracks(self) -> int:
        return self._session.get(
            url="https://api.vk.com/method/audio.get",
            params=[
                ('access_token', self._access_token),
                ('v', self._api_version)
            ]).json()['response']['count']

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
            url="https://api.vk.com/method/audio.get",
            params=[
                ('access_token', self._access_token),
                ('v', self._api_version),
                ('count', page_size),
                ('offset', self._offset)
            ])
        current_page_tracks = current_page_tracks.json()['response']['items']
        self._offset += page_size
        return [{'artist': l['artist'], 'title': l['title']} for l in current_page_tracks]
