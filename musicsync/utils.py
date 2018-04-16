from difflib import SequenceMatcher as SM

from .exceptions import AuthError, ClientError


def is_match(s1, s2):
    """
    Fuzzy matching of two strings
    Return True if probability of match is at least 80%
    """
    return SM(None, s1, s2).ratio() >= 0.80


def _raise_for_error(req):
    code, text = req.status_code, req.text
    if code >= 400:
        if code == 401 or code == 403:
            raise AuthError(f'Failed to authenticate with Spotify: {text}')
        raise ClientError(f'Spotify Error {code}: {text}')