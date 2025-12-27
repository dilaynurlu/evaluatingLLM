import pytest
import secrets
from requests.utils import get_auth_from_url

def test_get_auth_from_url_handles_empty_username_with_password():
    """
    Test that get_auth_from_url correctly extracts an empty username and the password
    when the username component is empty but the colon and password are present.
    
    Refinements:
    - Uses HTTPS.
    - Uses random password to avoid hardcoded secrets.
    - Masks assertions.
    """
    password = secrets.token_hex(8)
    url = f"https://:{password}@example.com/login"
    
    expected_auth = ("", password)
    actual_auth = get_auth_from_url(url)
    
    if actual_auth != expected_auth:
        raise AssertionError("Auth mismatch. Expected ('', password). (Password hidden)")
    
'''
Manually marked as assertion correct in csv, because test contains a custom assertion. Justnot recognized by the tool
'''