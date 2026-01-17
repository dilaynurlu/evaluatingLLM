
import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_special_chars():
    url = "http://foo%3Abar:baz%40qux@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("foo:bar", "baz@qux")
