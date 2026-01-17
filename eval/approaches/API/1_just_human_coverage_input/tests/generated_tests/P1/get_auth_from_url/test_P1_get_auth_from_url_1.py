import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_extracts_standard_credentials():
    """
    Test that username and password are correctly extracted from a standard URL
    containing both components separated by a colon.
    """
    url = "http://myuser:mypassword@example.com/resource"
    expected_auth = ("myuser", "mypassword")
    
    assert get_auth_from_url(url) == expected_auth