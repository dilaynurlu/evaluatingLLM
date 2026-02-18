import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_user():
    """Test extracting auth with empty username."""
    url = "http://:pass@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("", "pass")
