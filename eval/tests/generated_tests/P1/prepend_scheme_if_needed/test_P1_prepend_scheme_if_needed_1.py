import pytest
from unittest.mock import patch, MagicMock
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_no_scheme_host_only():
    """
    Test that a URL with no scheme (e.g., 'google.com') gets the default scheme prepended.
    This validates the logic where 'netloc' is missing/empty and the function swaps 'path' to 'netloc'.
    """
    url = "google.com"
    new_scheme = "http"
    
    # Simulate parse_url result:
    # scheme=None, auth=None, host=None, port=None, path='google.com', query='', fragment=''
    # We use empty strings for query/fragment to ensure urlunparse works correctly.
    # Importantly, netloc is absent (empty), triggering the swap logic.
    mock_parsed_items = (None, None, None, None, "google.com", "", "")
    
    with patch("requests.utils.parse_url") as mock_parse:
        # Create a mock object that behaves like the Url namedtuple + has .netloc attribute
        mock_obj = MagicMock()
        mock_obj.__iter__.side_effect = lambda: iter(mock_parsed_items)
        mock_obj.netloc = ""  # Simulate missing netloc
        
        mock_parse.return_value = mock_obj
        
        result = prepend_scheme_if_needed(url, new_scheme)
        
        # Expect: scheme added, path moved to netloc
        assert result == "http://google.com"
        mock_parse.assert_called_once_with(url)