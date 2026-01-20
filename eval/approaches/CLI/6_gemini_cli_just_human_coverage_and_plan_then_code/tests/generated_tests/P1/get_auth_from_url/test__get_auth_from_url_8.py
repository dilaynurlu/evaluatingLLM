import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_path_only_no_auth():
    url = "/path/to/resource"
    auth = get_auth_from_url(url)
    assert auth == ("", "")
