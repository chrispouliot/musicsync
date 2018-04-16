
import requests

from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth

from .config import logger, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from .exceptions import AuthError
from .utils import _raise_for_error

BASE_URL = "https://api.spotify.com/v1"
AUTHORIZE_URL = "https://accounts.spotify.com/api/token"


class SpotifyClientAuth:
    _client_secret = ""
    _client_id = ""
    _granted_token = ""
    _token_expiry_date = datetime.now()

    _session = None

    def __init__(self, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET):
        if not client_id and client_secret:
            raise AuthError("Invalid auth credentials provided")
        self._client_id, self._client_secret = client_id, client_secret

    @property
    def session(self):
        if not self._session:
            self._session = requests.Session()
        self._session.headers.update({
            "Authorization": "Bearer {token}".format(token=self._get_auth())
        })
        return self._session

    def _authenticate(self):
        data = {
            "grant_type": "client_credentials"
        }

        r = self._session.post(
            AUTHORIZE_URL,
            auth=HTTPBasicAuth(self._client_id, self._client_secret),
            data=data
        )
        _raise_for_error(r)

        body = r.json()
        expiry = body.get("expires_in")
        token = body.get("access_token")

        if not expiry or not token:
            logger.warning(
                "Failed to authenticate with Spotify. Invalid tokens returned. Status code %s",
                r.status_code
            )
            _raise_for_error(r)

        token_expiry = datetime.now() + timedelta(seconds=expiry)

        return token, token_expiry

    def _get_auth(self, re_auth=False):

        if self._token_expiry_date > datetime.now() and not re_auth:
            return self._granted_token

        self._granted_token, self._token_expiry_date = self._authenticate()
        return self._granted_token
