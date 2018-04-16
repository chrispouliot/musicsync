from .config import logger, SPOTIFY_USER_ID
from .serializers import Playlist
from .utils import _raise_for_error


PLAYLISTS_URL = f"https://api.spotify.com/v1/users/{SPOTIFY_USER_ID}/playlists"


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
