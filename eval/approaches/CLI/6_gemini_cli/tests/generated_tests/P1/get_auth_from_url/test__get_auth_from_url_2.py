import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_user_no_pass_explicit_empty():
    url = "http://user:@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("user", "")
