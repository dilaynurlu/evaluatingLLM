import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_pass():
    """Test extracting auth with empty password."""
    url = "http://user:@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("user", "")
