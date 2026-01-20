import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_at():
    # user%40:pass
    url = "http://user%40:pass@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("user@", "pass")
