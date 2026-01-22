import pytest
from requests.utils import get_auth_from_url

def test_get_auth_partial_credentials():
    """
    Test edge cases where either the username or the password component 
    is empty within the URL structure.
    
    Refinements based on critique:
    - Renamed from test_get_auth_empty_password to cover wider scope.
    - Added verification for empty username with valid password (:password@host).
    """
    # Case 1: Empty password (user:@host)
    url_empty_pass = "https://TEST_USER:@dashboard.example.com"
    assert get_auth_from_url(url_empty_pass) == ("TEST_USER", "")

    # Case 2: Empty username (:password@host)
    url_empty_user = "https://:TEST_KEY@dashboard.example.com"
    assert get_auth_from_url(url_empty_user) == ("", "TEST_KEY")