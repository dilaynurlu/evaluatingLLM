import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded():
    # user%40domain:pass%23word
    url = "http://user%40domain:pass%23word@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("user@domain", "pass#word")
