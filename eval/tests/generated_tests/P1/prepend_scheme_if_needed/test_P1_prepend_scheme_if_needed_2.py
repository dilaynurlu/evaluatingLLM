import pytest
from unittest.mock import patch, MagicMock
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_preserve_existing():
    """
    Test that if a URL already has a scheme, it is preserved and the new scheme is ignored.
    """
    url = "https://google.com"
    new_scheme = "http"
    
    # Simulate parse_url result where scheme is already 'https'
    mock_parsed_items = ("https", None, "google.com", None, "", "", "")
    
    with patch("requests.utils.parse_url") as mock_parse:
        mock_obj = MagicMock()
        mock_obj.__iter__.side_effect = lambda: iter(mock_parsed_items)
        mock_obj.netloc = "google.com"
        
        mock_parse.return_value = mock_obj
        
        result = prepend_scheme_if_needed(url, new_scheme)
        
        assert result == "https://google.com"