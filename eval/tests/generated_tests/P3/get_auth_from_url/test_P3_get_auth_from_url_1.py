import pytest
from requests.utils import get_auth_from_url

def test_get_auth_basic_credentials():
    """
    Test that username and password are extracted correctly from a URL.
    
    Refinements based on critique:
    - Uses 'postgres' scheme to ensure logic is scheme-independent.
    - Uses placeholders TEST_USER and TEST_KEY to avoid triggering 
      secret scanners or leaking 'real' password patterns in logs.
    """
    # Use a custom or non-http scheme to ensure parsing is protocol-agnostic
    url = "postgres://TEST_USER:TEST_KEY@db.example.com/production"
    expected_auth = ("TEST_USER", "TEST_KEY")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth