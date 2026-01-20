
import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_at_in_password():
    # If the password contains @ it must be percent encoded, otherwise it terminates the authority
    # But if someone puts it in, browsers usually pick the last @
    # urlparse picks the last @ as the separator
    url = "http://user:p@ss@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("user", "p@ss")
