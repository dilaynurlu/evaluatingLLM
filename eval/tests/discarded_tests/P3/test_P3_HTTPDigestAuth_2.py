import pytest
from unittest.mock import Mock, MagicMock, patch
from requests.auth import HTTPDigestAuth
from requests import PreparedRequest

def test_digest_auth_handle_401_md5_special_chars():
    """
    Test handling of a 401 response with special characters in credentials and realm.
    Verifies that the Authorization header correctly quotes/escapes values.
    Also ensures response content is consumed to prevents connection pool leaks.
    """
    # Username with quote, password with backslash
    user = 'user"name'
    password = 'pass\\word'
    auth = HTTPDigestAuth(user, password)
    
    # Setup initial request using PreparedRequest to test copying logic
    initial_request = PreparedRequest()
    initial_request.prepare(
        method="GET",
        url="http://example.org/resource",
        headers={}
    )
    
    # Setup 401 response
    response = Mock()
    response.status_code = 401
    # Realm containing a quote
    response.headers = {
        "www-authenticate": 'Digest realm="my\\"realm", nonce="nonce123", qop="auth"'
    }
    response.is_redirect = False
    # Content that must be consumed
    response.content = b"Auth Required"
    response.request = initial_request
    response.connection = Mock()
    
    # Mock the result of the resent request
    resent_response = Mock()
    resent_response.history = []
    response.connection.send.return_value = resent_response
    
    # Initialize state
    auth(initial_request)
    
    with patch("requests.auth.extract_cookies_to_jar"):
        result = auth.handle_401(response)
        
        assert result == resent_response
        
        # Verify response content was accessed (consumed)
        # We verify that the mock's content attribute was accessed during the process
        # This is critical for releasing the connection back to the pool
        assert isinstance(response.content, bytes) 
        
        # Check Authorization header for correct escaping
        args, _ = response.connection.send.call_args
        sent_request = args[0]
        auth_header = sent_request.headers.get("Authorization")
        
        # The username should be quoted. Depending on implementation, quote might be escaped.
        # Standard requests behavior puts it in quotes.
        assert 'username="user\\"name"' in auth_header
        assert 'realm="my\\"realm"' in auth_header
        assert 'nonce="nonce123"' in auth_header
        assert 'uri="/resource"' in auth_header


'''
Assertion failed:

# Check Authorization header for correct escaping
            args, _ = response.connection.send.call_args
            sent_request = args[0]
            auth_header = sent_request.headers.get("Authorization")
    
            # The username should be quoted. Depending on implementation, quote might be escaped.
            # Standard requests behavior puts it in quotes.
>           assert 'username="user\\"name"' in auth_header
E           assert 'username="user\\"name"' in 'Digest username="user"name", realm="my"realm", nonce="nonce123", uri="/resource", response="aa6105ed2504f4ecab8ac1065326f683", qop="auth", nc=00000001, cnonce="316c7922fddc891f"'

eval/tests/generated_tests/P3/HTTPDigestAuth/test_P3_HTTPDigestAuth_2.py:63: AssertionError
'''