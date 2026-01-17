import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_decodes_utf8_sequences():
    """
    Test that UTF-8 percent-encoded sequences in the URL auth components 
    are correctly decoded to unicode characters.
    """
    # 'café' -> 'caf%C3%A9'
    # 'lattes' -> 'lattes'
    url = "http://caf%C3%A9:lattes@example.com"
    expected_auth = ("café", "lattes")
    
    assert get_auth_from_url(url) == expected_auth