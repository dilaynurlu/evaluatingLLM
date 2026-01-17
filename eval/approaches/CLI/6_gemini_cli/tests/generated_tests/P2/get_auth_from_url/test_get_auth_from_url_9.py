import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_colon():
    # user:pass%3Aword
    url = "http://user:pass%3Aword@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("user", "pass:word")
