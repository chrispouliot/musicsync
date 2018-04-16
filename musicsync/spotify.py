import requests

from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

from .config import logger, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_USER_ID
from .exceptions import AuthError, ClientError
from .serializers import Playlist


BASE_URL = "https://api.spotify.com/v1"
AUTHORIZE_URL = "https://accounts.spotify.com/api/token"
PLAYLISTS_URL = f"https://api.spotify.com/v1/users/{SPOTIFY_USER_ID}/playlists"


def _raise_for_error(req):
    code, text = req.status_code, req.text
    if code >= 400:
        if code == 401 or code == 403:
            raise AuthError(f'Failed to authenticate with Spotify: {text}')
        raise ClientError(f'Spotify Error {code}: {text}')


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


class Spotify:
    _auth = None

    def __init__(self, auth):
        self._auth = auth

    def _get(self, url):
        r = self._auth.session.get(url)
        _raise_for_error(r)

        return r.json()

    def get_playlist(self, name):
        user_playlists = self._get(PLAYLISTS_URL)
        playlist = None

        # TODO: Handle pagination of results
        for user_playlist in user_playlists['items']:
            if user_playlist['name'] == name:
                playlist = user_playlist
                break

        if not playlist:
            logger.warning("Unable to find playlist '{}'. Is it public?".format(name))
            return None

        # Exchange the minified playlist for a full playlist
        playlist = self._get(playlist['href'])

        # Once we've found the playlist, get all it's tracks
        next_results_url = playlist['tracks']['next']

        # Spotify paginates long results
        while next_results_url:
            paginated_results = self._get(next_results_url)
            next_results_url = paginated_results['next']

            playlist['tracks']['items'] += paginated_results['items']

        return Playlist.from_spotify(playlist)

    def create_playlist(self, playlist_obj, override):
        return None
