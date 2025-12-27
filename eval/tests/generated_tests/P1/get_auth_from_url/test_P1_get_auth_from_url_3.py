import pytest
from unittest.mock import patch
from requests.utils import get_auth_from_url

def test_get_auth_from_url_handles_attribute_error_on_parse_result():
    """
    Test that get_auth_from_url returns empty strings when an AttributeError occurs.
    This scenario simulates urlparse returning None or an object missing required attributes,
    triggering an AttributeError when accessing .username or .password.
    """
    with patch('requests.utils.urlparse') as mock_urlparse:
        
        # Setup mock to return None. 
        # Accessing None.username inside the function will raise AttributeError.
        mock_urlparse.return_value = None
        
        # Execute the target function
        result = get_auth_from_url("http://broken-url")
        
        # Assertions
        # The AttributeError should be caught and converted to empty strings
        assert result == ('', '')
        
        mock_urlparse.assert_called_once()