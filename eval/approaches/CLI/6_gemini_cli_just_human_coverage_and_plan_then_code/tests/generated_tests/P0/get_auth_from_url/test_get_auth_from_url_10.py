
import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_unicode():
    url = "http://üser:påss@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("üser", "påss")
