import requests

from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

from .config import logger, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_USER_ID
from .exceptions import AuthError, ClientError
from .serializers import Playlist


BASE_URL = "https://api.spotify.com/v1"
AUTHORIZE_URL = "https://accounts.spotify.com/api/token"
PLAYLISTS_URL = f"https://api.spotify.com/v1/users/{SPOTIFY_USER_ID}/playlists"


class Spotify(object):
    _granted_token = ""
    _token_expiry_date = datetime.now()

    def _get_auth(self, re_auth=False):

        if self._token_expiry_date > datetime.now() and not re_auth:
            return self._granted_token

        self._granted_token, self._token_expiry_date = self._authenticate()
        return self._granted_token

    def _authenticate(self):
        data = {
            "grant_type": "client_credentials"
        }

        r = requests.post(AUTHORIZE_URL, auth=HTTPBasicAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET), data=data)
        self._raise_for_error(r)

        body = r.json()
        expiry = body.get("expires_in")
        token = body.get("access_token")

        if not expiry or not token:
            logger.warning(
                "Failed to authenticate with Spotify. Invalid tokens returned. Status code %s",
                r.status_code
            )
            self._raise_for_error(r)

        token_expiry = datetime.now() + timedelta(seconds=expiry)

        return token, token_expiry

    def _get(self, url):
        token = self._get_auth()
        headers = {"Authorization": "Bearer {token}".format(token=token)}

        r = requests.get(url, headers=headers)
        self._raise_for_error(r)

        return r.json()

    def _raise_for_error(self, req):
        code, text = req.status_code, req.text
        if code >= 400:
            if code == 401 or code == 403:
                raise AuthError(f'Failed to authenticate with Spotify: {text}')
            raise ClientError(f'Spotify Error {code}: {text}')

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
