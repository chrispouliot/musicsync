from .auth import GPMClientAuth, SpotifyClientAuth
from .gpm import GPM
from .spotify import Spotify


class MusicClient:
    DEFAULT_AUTH = None
    CLIENT = None

    _client = None

    def __init__(self, auth=None):
        if not auth:
            # Can't initialize as default arg because it would require env vars on import
            auth = self.DEFAULT_AUTH()
        self._client = self.CLIENT(auth)

    def get_playlist(self, name):
        '''
        Retrieve a playlist from the music client

        :param str name: The name of the playlist to retrieve
        :return: The playlist
        :rtype: Playlist serializer object
        '''
        return self._client.get_playlist(name)

    def create_playlist(self, playlist, override_existing=True):
        '''
        Create a playlist from the music client

        :param playlist: The playlist to be created
        :type playlist: Playlist serializer object
        :param bool override_existing: Delete playlist if it already exists
        :return: Number of songs matched
        :rtype: Int
        '''
        return self._client.create_playlist(playlist, override_existing)


class SpotifyClient(MusicClient):
    DEFAULT_AUTH = SpotifyClientAuth
    CLIENT = Spotify


class GPMClient(MusicClient):
    DEFAULT_AUTH = GPMClientAuth
    CLIENT = GPM
