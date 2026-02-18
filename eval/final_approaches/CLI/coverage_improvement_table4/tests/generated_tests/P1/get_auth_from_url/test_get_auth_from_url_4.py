import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_invalid_input():
    """Test behavior with invalid input (should return empty strings)."""
    # Passing None to urlparse might raise TypeError/AttributeError depending on implementation details
    # which get_auth_from_url catches.
    # urlparse(None) -> TypeError or AttributeError in 3.11?
    # Actually urlparse(None) raises TypeError.
    # get_auth_from_url catches (AttributeError, TypeError).
    auth = get_auth_from_url(None)
    assert auth == ("", "")
