import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_credentials():
    """
    Test extraction of percent-encoded characters in username and password.
    'us@er' -> 'us%40er'
    'pa/ss' -> 'pa%2Fss'
    """
    url = "https://us%40er:pa%2Fss@example.com/path"
    expected_auth = ("us@er", "pa/ss")
    
    assert get_auth_from_url(url) == expected_auth