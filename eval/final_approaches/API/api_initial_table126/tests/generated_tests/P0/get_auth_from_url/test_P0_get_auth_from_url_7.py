import pytest
from requests.utils import get_auth_from_url

def test_get_auth_unicode_characters():
    """
    Test extracting username and password containing Unicode characters.
    Note: Browsers and libraries often percent-encode unicode in URLs, 
    but get_auth_from_url handles the unquoting.
    
    Input encoded: u%C3%BCser (uüser), p%C3%A5ss (påss)
    """
    url = "http://u%C3%BCser:p%C3%A5ss@example.com"
    expected_auth = ("uüser", "påss")
    
    assert get_auth_from_url(url) == expected_auth