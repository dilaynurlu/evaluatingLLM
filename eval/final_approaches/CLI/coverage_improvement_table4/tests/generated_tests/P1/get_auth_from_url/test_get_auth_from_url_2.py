import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_no_auth():
    """Test extracting auth from a URL without auth credentials."""
    url = "http://example.com"
    auth = get_auth_from_url(url)
    assert auth == ("", "")
