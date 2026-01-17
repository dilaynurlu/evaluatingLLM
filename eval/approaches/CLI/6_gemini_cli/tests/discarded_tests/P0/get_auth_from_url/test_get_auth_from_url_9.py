
import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_non_url():
    url = "not_a_url"
    auth = get_auth_from_url(url)
    assert auth == (None, None)
