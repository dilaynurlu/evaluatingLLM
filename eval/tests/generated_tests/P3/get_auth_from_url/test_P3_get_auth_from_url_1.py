import pytest
import secrets
from requests.utils import get_auth_from_url

def test_get_auth_from_url_returns_correct_credentials_for_standard_url():
    """
    Test that get_auth_from_url correctly extracts plain text username and password
    from a standard HTTPS URL.
    
    Refinements:
    - Uses HTTPS to simulate a secure environment.
    - Uses random strings for credentials to avoid hardcoded secrets.
    - Implements manual assertion logic to mask credentials in CI logs upon failure.
    """
    # Generate random credentials
    username = secrets.token_hex(8)
    password = secrets.token_hex(8)
    
    # Use HTTPS to reinforce secure practices
    url = f"https://{username}:{password}@example.com/resource"
    expected_auth = (username, password)
    
    actual_auth = get_auth_from_url(url)
    
    # Custom assertion to prevent leaking credentials in pytest output
    if actual_auth != expected_auth:
        raise AssertionError("Parsed credentials do not match expected values. (Values hidden for security)")
    

'''
Manually marked as assertion correct in csv, because test contains a custom assertion. Justnot recognized by the tool
'''