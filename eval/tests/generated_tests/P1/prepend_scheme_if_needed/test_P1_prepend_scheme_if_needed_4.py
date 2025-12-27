import pytest
from unittest.mock import patch, MagicMock
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_netloc_already_parsed():
    """
    Test handling of URLs starting with // (scheme-relative URLs).
    In this case, parse_url usually identifies the netloc correctly, so the swap logic should be skipped.
    """
    url = "//google.com"
    new_scheme = "http"
    
    # Simulate parse_url result where scheme is None but netloc is already found.
    mock_parsed_items = (None, None, "google.com", None, "", "", "")
    
    with patch("requests.utils.parse_url") as mock_parse:
        mock_obj = MagicMock()
        mock_obj.__iter__.side_effect = lambda: iter(mock_parsed_items)
        mock_obj.netloc = "google.com"  # Netloc present
        
        mock_parse.return_value = mock_obj
        
        result = prepend_scheme_if_needed(url, new_scheme)
        
        # Logic trace:
        # 1. netloc is present -> NO swap.
        # 2. scheme added.
        assert result == "http://google.com"