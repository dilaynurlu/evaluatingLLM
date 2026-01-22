import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_password():
    """
    Test extraction when password is provided as an empty string 
    (indicated by a trailing colon after the username).
    """
    # "user:" implies username="user" and password=""
    url = "http://user:@example.com/dashboard"
    expected_auth = ("user", "")
    
    assert get_auth_from_url(url) == expected_auth