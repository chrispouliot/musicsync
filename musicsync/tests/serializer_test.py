import json
import os

from unittest import TestCase

from musicsync.serializers import Playlist


_fixtures_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


class TestSerializers(TestCase):
    def setUp(self):
        with open(os.path.join(_fixtures_path, 'spotify_playlist.json')) as f:
            self._spotify_json = json.load(f)
        with open(os.path.join(_fixtures_path, 'gpm_playlist.json')) as f:
            self._gpm_json = json.load(f)

    def test_valid_spotify_playlist(self):
        serialized_playlist = Playlist.from_spotify(self._spotify_json)
        self.assertEqual(serialized_playlist.title, "Discover Weekly")
        self.assertEqual(len(serialized_playlist.songs), 2)

    def test_valid_gpm_playlist(self):
        serialized_playlist = Playlist.from_gpm(self._gpm_json)
        self.assertEqual(serialized_playlist.title, "Discover Weekly")
        self.assertEqual(len(serialized_playlist.songs), 2)
