from requests.utils import get_auth_from_url
from unittest.mock import patch

def test_get_auth_from_url_5():
    # Force an exception to test the except block
    # We can mock urlparse to return an object that raises AttributeError on .username
    
    with patch("requests.utils.urlparse") as mock_parse:
        class MockParsed:
            @property
            def username(self):
                raise AttributeError("fail")
        mock_parse.return_value = MockParsed()
        
        url = "http://example.com"
        auth = get_auth_from_url(url)
        assert auth == ("", "")