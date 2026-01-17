import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_non_http_schemes():
    """
    Test extraction with non-HTTP schemes (e.g., ftp://).
    
    This ensures the function is protocol-agnostic regarding the authority section
    and correctly handles cases where the username is empty but a password is provided.
    """
    # FTP scheme, empty username, secret password
    # :secret implies username='' and password='secret'
    url = "ftp://:secret@ftp.example.com/"
    expected_auth = ("", "secret")
    
    assert get_auth_from_url(url) == expected_auth