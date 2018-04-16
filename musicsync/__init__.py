from .copy import spotify_gpm_copy
from .musicclient import GPMClient, SpotifyClient
from .auth import SpotifyClientAuth

# Appease Flake8
(spotify_gpm_copy, GPMClient, SpotifyClient, SpotifyClientAuth)
