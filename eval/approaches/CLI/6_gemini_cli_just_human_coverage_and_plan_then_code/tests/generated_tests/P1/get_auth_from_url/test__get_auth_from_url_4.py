import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_username():
    url = "http://us%40er:pass@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("us@er", "pass")
