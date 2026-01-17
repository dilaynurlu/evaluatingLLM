import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_credentials():
    """
    Test that percent-encoded characters in the username and password
    are correctly unquoted in the returned tuple.
    Input: user='u@ser' (encoded as u%40ser), pass='p@ss' (encoded as p%40ss).
    """
    url = "http://u%40ser:p%40ss@example.com/"
    expected_auth = ("u@ser", "p@ss")
    
    assert get_auth_from_url(url) == expected_auth