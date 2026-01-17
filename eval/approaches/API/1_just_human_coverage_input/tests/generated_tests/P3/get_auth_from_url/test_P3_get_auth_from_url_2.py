import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_complex_encoded_credentials():
    """
    Test extraction of credentials containing:
    1. Percent-encoded reserved characters (e.g., / -> %2F).
    2. Unicode characters encoded (e.g., 'user☃' -> 'user%E2%98%83').
    
    Ensures that the parser correctly decodes these values and does not
    prematurely terminate parsing on reserved characters inside the password.
    """
    # 'user☃' (Snowman \u2603) : 'p@ss/word' (with slash encoded as %2F)
    url = "https://user%E2%98%83:p%40ss%2Fword@example.com/api"
    expected_auth = ("user\u2603", "p@ss/word")
    
    assert get_auth_from_url(url) == expected_auth