from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_credentials():
    """
    Test URL with percent-encoded characters and Unicode.
    Verifies that `unquote` correctly decodes special chars and UTF-8 sequences.
    
    Input:
    Username: 'üser' (encoded as %C3%BCser)
    Password: 's@cret' (encoded as s%40cret)
    """
    url = "http://%C3%BCser:s%40cret@example.com"
    result = get_auth_from_url(url)
    assert result == ("üser", "s@cret")