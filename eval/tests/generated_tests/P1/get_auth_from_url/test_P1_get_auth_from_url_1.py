import pytest
from unittest.mock import patch, Mock
from requests.utils import get_auth_from_url

def test_get_auth_from_url_extracts_and_decodes_valid_credentials():
    """
    Test that get_auth_from_url correctly extracts username and password 
    from a URL and unquotes them using the internal unquote function.
    """
    # Patch urlparse and unquote within requests.utils to isolate the function logic
    with patch('requests.utils.urlparse') as mock_urlparse, \
         patch('requests.utils.unquote') as mock_unquote:
        
        # Setup the mock object returned by urlparse
        mock_parsed_result = Mock()
        # Set encoded attributes to verify unquoting logic is triggered
        mock_parsed_result.username = 'usr%40name'
        mock_parsed_result.password = 'p%40ssword'
        mock_urlparse.return_value = mock_parsed_result
        
        # Define side effect for unquote to simulate decoding
        def unquote_side_effect(value):
            if value == 'usr%40name':
                return 'usr@name'
            if value == 'p%40ssword':
                return 'p@ssword'
            return value
            
        mock_unquote.side_effect = unquote_side_effect
        
        # Execute the target function
        target_url = "http://usr%40name:p%40ssword@example.com"
        result = get_auth_from_url(target_url)
        
        # Assertions
        assert result == ('usr@name', 'p@ssword')
        
        # Verify interactions
        mock_urlparse.assert_called_once_with(target_url)
        assert mock_unquote.call_count == 2
        mock_unquote.assert_any_call('usr%40name')
        mock_unquote.assert_any_call('p%40ssword')