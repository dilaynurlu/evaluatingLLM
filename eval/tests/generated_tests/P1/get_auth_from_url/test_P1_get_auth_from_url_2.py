import pytest
from unittest.mock import patch, Mock
from requests.utils import get_auth_from_url

def test_get_auth_from_url_handles_type_error_on_missing_components():
    """
    Test that get_auth_from_url returns empty strings when a TypeError occurs,
    specifically when one of the auth components is None (e.g., missing password),
    which causes unquote() to raise TypeError.
    """
    with patch('requests.utils.urlparse') as mock_urlparse, \
         patch('requests.utils.unquote') as mock_unquote:
        
        # Setup the mock result to have a username but no password (None)
        mock_parsed_result = Mock()
        mock_parsed_result.username = 'user'
        mock_parsed_result.password = None 
        mock_urlparse.return_value = mock_parsed_result
        
        # Configure unquote to raise TypeError when receiving None
        # This mirrors the behavior of urllib.parse.unquote in Python 3
        def unquote_side_effect(value):
            if value is None:
                raise TypeError("expected string or bytes-like object")
            return value
            
        mock_unquote.side_effect = unquote_side_effect
        
        # Execute the target function
        # The URL input here is arbitrary as we mocked urlparse
        result = get_auth_from_url("http://user@example.com")
        
        # Assertions
        # Expect empty tuple due to exception handling
        assert result == ('', '')
        
        # Verify we attempted to parse
        mock_urlparse.assert_called_once()