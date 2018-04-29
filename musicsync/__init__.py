from .copy import spotify_gpm_copy
from .musicclient import GPMClient, SpotifyClient
from .auth import GPMClientAuth, SpotifyClientAuth, SpotifyOAuth

# Appease Flake8
(spotify_gpm_copy, GPMClient, GPMClientAuth,  SpotifyClient, SpotifyClientAuth, SpotifyOAuth)
