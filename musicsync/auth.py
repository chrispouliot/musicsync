
import requests

from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth
from requests import Request

from .config import logger, \
    GPM_APP_PASSWORD, \
    GPM_EMAIL_ADDRESS, \
    SPOTIFY_CLIENT_ID, \
    SPOTIFY_CLIENT_SECRET
from .exceptions import AuthError
from .utils import _raise_for_error

BASE_URL = 'https://api.spotify.com/v1'
AUTHORIZE_TOKEN_URL = 'https://accounts.spotify.com/api/token'
OAUTH_USER_REQUEST_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize/'


class BaseSpotifyAuth:
    @property
    def session(self):
        raise NotImplementedError()


class GPMClientAuth:
    email = ""
    password = ""

    def __init__(self, email=GPM_EMAIL_ADDRESS, password=GPM_APP_PASSWORD):
        self.email, self.password = email, password


class SpotifyClientAuth(BaseSpotifyAuth):
    _client_secret = ""
    _client_id = ""
    _granted_token = ""
    _token_expiry_date = datetime.now()
    _session = None

    def __init__(self, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET):
        if not (client_id and client_secret):
            raise AuthError("Invalid auth credentials provided")
        self._client_id, self._client_secret = client_id, client_secret

    @property
    def session(self):
        if not self._session:
            self._session = requests.Session()
        self._session.headers.update({
            'Authorization': f"Bearer {self._get_auth()}"
        })
        return self._session

    def _get_auth(self, re_auth=False):

        if self._token_expiry_date > datetime.now() and not re_auth:
            return self._granted_token

        self._granted_token, self._token_expiry_date = self._authenticate()
        return self._granted_token

    def _authenticate(self):
        data = {
            'grant_type': 'client_credentials'
        }

        r = self._session.post(
            AUTHORIZE_TOKEN_URL,
            auth=HTTPBasicAuth(self._client_id, self._client_secret),
            data=data
        )
        _raise_for_error(r)

        body = r.json()
        expiry = body.get('expires_in')
        token = body.get('access_token')

        if not expiry or not token:
            logger.warning(
                "Failed to authenticate with Spotify. Invalid tokens returned. Status code %s",
                r.status_code
            )
            _raise_for_error(r)

        token_expiry = datetime.now() + timedelta(seconds=expiry)

        return token, token_expiry


class SpotifyOAuth(BaseSpotifyAuth):
    _client_secret = ""
    _client_id = ""
    _oauth_code = ""
    _refresh_token = ""
    _granted_token = ""
    _token_expiry_date = datetime.now()
    _session = None

    def __init__(
            self,
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            code='',
            redirect_uri=''):
        if not (client_id and client_secret and code and redirect_uri):
            raise AuthError("Invalid auth credentials provided")
        self._client_id = client_id
        self._client_secret = client_secret
        self._oauth_code = code
        self._redirect_uri = redirect_uri

    @property
    def session(self):
        if not self._session:
            self._session = requests.Session()
        self._session.headers.update({
            'Authorization': f"Bearer {self._get_auth()}"
        })
        return self._session

    # TODO: Could make this a non-static func? How keep the Spotify client using this Auth after a redirect?
    @staticmethod
    def get_oauth_url(client_id, redirect_uri, state):
        payload = {
            'client_id': client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'state': state
        }
        return Request(
            'GET',
            OAUTH_USER_REQUEST_AUTHORIZE_URL,
            params=payload
        ).prepare().url

    def _get_auth(self, re_auth=False):
        token_expired = self._token_expiry_date > datetime.now()
        if token_expired and not re_auth:
            return self._granted_token

        self._granted_token, self._token_expiry_date, self._refresh_token = self._authenticate(refresh=token_expired)
        return self._granted_token

    def _authenticate(self, refresh=False):
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self._refresh_token,
            'redirect_uri': self._redirect_uri
        }

        if not refresh:
            data['grant_type'] = 'authorization_code'
            data['code'] = self._oauth_code,

        r = self._session.post(
            AUTHORIZE_TOKEN_URL,
            auth=HTTPBasicAuth(self._client_id, self._client_secret),
            data=data
        )
        _raise_for_error(r)

        body = r.json()
        expiry = body.get('expires_in')
        token = body.get('access_token')
        refresh_token = body.get('refresh_token')

        if not (expiry and token and refresh_token):
            logger.warning(
                "Failed to authenticate with Spotify. Invalid tokens returned. Status code %s",
                r.status_code
            )
            _raise_for_error(r)

        token_expiry = datetime.now() + timedelta(seconds=expiry)

        return token, token_expiry, refresh_token
