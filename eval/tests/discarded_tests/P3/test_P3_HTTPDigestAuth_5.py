import pytest
from unittest.mock import Mock, MagicMock, patch
from requests.auth import HTTPDigestAuth
from requests import PreparedRequest

def test_digest_auth_handle_stale_nonce():
    """
    Test handling of the 'stale=true' directive in the challenge.
    When stale=true is present, the client should retry the request immediately
    with the new nonce, without counting it as an authentication failure (recursion check).
    """
    auth = HTTPDigestAuth("user", "pass")
    
    initial_request = PreparedRequest()
    initial_request.prepare(method="GET", url="http://example.com")
    
    # Response indicating the previous nonce was stale
    response = Mock()
    response.status_code = 401
    response.headers = {
        "www-authenticate": 'Digest realm="realm", nonce="new_nonce", stale=true, qop="auth"'
    }
    response.is_redirect = False
    response.content = b""
    response.request = initial_request
    response.connection = Mock()
    response.connection.send.return_value = Mock(history=[])
    
    auth(initial_request)
    
    # Simulate that we are at the retry limit (e.g., previous attempt just failed)
    # If stale=true is not handled correctly, handle_401 would see calls=2 and stop.
    auth._thread_local.num_401_calls = 2
    
    with patch("requests.auth.extract_cookies_to_jar"):
        auth.handle_401(response)
        
        # Verify a new request was sent despite num_401_calls being 2 originally
        assert response.connection.send.called
        sent_req = response.connection.send.call_args[0][0]
        auth_header = sent_req.headers['Authorization']
        
        # Verify the new nonce was used
        assert 'nonce="new_nonce"' in auth_header
        
        # Verify nc (nonce count) was reset for the new nonce
        assert 'nc=00000001' in auth_header

'''
Assertion failed:


# Simulate that we are at the retry limit (e.g., previous attempt just failed)
        # If stale=true is not handled correctly, handle_401 would see calls=2 and stop.
        auth._thread_local.num_401_calls = 2
    
        with patch("requests.auth.extract_cookies_to_jar"):
            auth.handle_401(response)
    
            # Verify a new request was sent despite num_401_calls being 2 originally
>           assert response.connection.send.called
E           AssertionError: assert False
E            +  where False = <Mock name='mock.connection.send' id='281473290659408'>.called
E            +    where <Mock name='mock.connection.send' id='281473290659408'> = <Mock name='mock.connection' id='281473290658640'>.send
E            +      where <Mock name='mock.connection' id='281473290658640'> = <Mock id='281473290658448'>.connection

eval/tests/generated_tests/P3/HTTPDigestAuth/test_P3_HTTPDigestAuth_5.py:39: AssertionError
'''