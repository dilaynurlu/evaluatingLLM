from unittest.mock import patch, MagicMock
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_legacy_parsing_defect_swap():
    """
    Test the branch where parsing fails to identify a netloc (common in some urlparse versions),
    causing the function to swap path and netloc.
    """
    url = "example.com"
    new_scheme = "ftp"
    
    # We mock parse_url to simulate a "defect" where the host is parsed as the path
    # and netloc is empty.
    with patch('requests.utils.parse_url') as mock_parse:
        # parsed unpacking: scheme, auth, host, port, path, query, fragment
        scheme = None
        auth = None
        host = None
        port = None
        path = "example.com"  # Host ended up in path
        query = ""
        fragment = ""
        
        mock_parsed = MagicMock()
        mock_parsed.__iter__.return_value = iter([scheme, auth, host, port, path, query, fragment])
        mock_parsed.netloc = ""  # Empty netloc triggers the swap logic
        
        mock_parse.return_value = mock_parsed
        
        result = prepend_scheme_if_needed(url, new_scheme)
        
        # Logic: netloc becomes 'example.com', path becomes ''
        assert result == "ftp://example.com"