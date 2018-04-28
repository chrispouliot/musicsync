from unittest import TestCase

from musicsync.auth import \
    SpotifyClientAuth, \
    SpotifyOAuth, \
    OAUTH_USER_REQUEST_AUTHORIZE_URL
from musicsync.exceptions import AuthError


class TestClientAuth(TestCase):

    def test_invalid_auth_creds(self):
        with self.assertRaises(AuthError):
            SpotifyClientAuth(client_id=None, client_secret=None)


class TestOAuth(TestCase):

    def test_invalid_auth_creds(self):
        with self.assertRaises(AuthError):
            SpotifyOAuth(client_id=None, client_secret=None)

    def test_get_oauth_url(self):
        client_id = 'abc123'
        redirect_uri = 'test'
        state = 'state'
        expected_url = f"{OAUTH_USER_REQUEST_AUTHORIZE_URL}?" \
            f"client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&state={state}"
        req = SpotifyOAuth.get_oauth_req(client_id, redirect_uri, state)

        self.assertEqual(expected_url, req.url)
