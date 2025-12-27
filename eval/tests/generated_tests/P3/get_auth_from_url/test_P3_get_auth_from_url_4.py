import pytest
import secrets
from requests.utils import get_auth_from_url

def test_get_auth_from_url_returns_empty_tuple_when_password_component_is_missing():
    """
    Test behavior when a username is provided without a password delimiter (colon).
    
    Refinements:
    - Uses HTTPS.
    - Uses random username.
    - Documents the library behavior where missing the password delimiter results
      in the entire auth component being discarded.
    """
    username = secrets.token_hex(5)
    # URL has user but no colon/password
    url = f"https://{username}@example.com/"
    
    # Current library implementation catches the TypeError from unquote(None)
    # and returns empty strings, discarding the username.
    expected_auth = ("", "")
    
    assert get_auth_from_url(url) == expected_auth