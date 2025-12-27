from unittest.mock import patch, MagicMock
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_constructs_auth():
    """
    Test that if parse_url returns an auth component but excludes it from netloc,
    prepend_scheme_if_needed correctly reconstructs the netloc with auth.
    """
    url = "user:pass@example.com"
    new_scheme = "https"
    
    # We mock parse_url to control the internal structure returned
    # simulating a parser that separates auth from netloc (or netloc doesn't include it yet)
    with patch('requests.utils.parse_url') as mock_parse:
        # parsed unpacking: scheme, auth, host, port, path, query, fragment
        scheme = None
        auth = "user:pass"
        host = "example.com"
        port = None
        path = ""
        query = ""
        fragment = ""
        
        # Mock object acting as the namedtuple/Url object
        mock_parsed = MagicMock()
        mock_parsed.__iter__.return_value = iter([scheme, auth, host, port, path, query, fragment])
        # Assume netloc is just the host in this scenario (to trigger the joining logic)
        mock_parsed.netloc = "example.com"
        
        mock_parse.return_value = mock_parsed
        
        result = prepend_scheme_if_needed(url, new_scheme)
        
        # Expectation: scheme + auth@netloc + path ...
        assert result == "https://user:pass@example.com"