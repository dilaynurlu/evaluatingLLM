import pytest
import secrets
from requests.utils import get_auth_from_url

def test_get_auth_from_url_handles_empty_password_with_delimiter():
    """
    Test that get_auth_from_url correctly extracts the username and an empty password
    when the password delimiter (colon) is present but no password follows.
    
    Refinements:
    - Uses HTTPS.
    - Uses random username to avoid hardcoding.
    - Masks assertion to protect the username in logs.
    """
    username = secrets.token_hex(6)
    url = f"https://{username}:@example.com/data"
    
    expected_auth = (username, "")
    actual_auth = get_auth_from_url(url)
    
    if actual_auth != expected_auth:
        # We can safely show that the password expectation was empty, but hide the username
        raise AssertionError("Auth mismatch. Expected (username, '') but got mismatch. (Username hidden)")
    
'''
Manually marked as assertion correct in csv, because test contains a custom assertion. Justnot recognized by the tool
'''