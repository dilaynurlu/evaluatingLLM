import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth

def test_nonce_count_increment():
    """
    Test that reusing the same nonce across requests increments the nonce count (nc).
    """
    auth = HTTPDigestAuth("user", "pass")
    nonce = "common_nonce"
    
    # --- Request 1 ---
    req1 = Mock()
    req1.headers = {}
    req1._cookies = Mock()
    req1.copy.return_value = Mock(headers={}, method="GET", url="http://a.com")
    
    resp1 = Mock()
    resp1.status_code = 401
    resp1.headers = {
        "www-authenticate": f'Digest realm="r", nonce="{nonce}", qop="auth"'
    }
    resp1.request = req1
    resp1.connection.send.return_value = Mock(history=[])
    
    with patch("requests.auth.extract_cookies_to_jar"):
        auth(req1)
        auth.handle_401(resp1)
        
    # Check that state recorded the nonce
    assert auth._thread_local.last_nonce == nonce
    assert auth._thread_local.nonce_count == 1
    
    # --- Request 2 (Same Auth instance) ---
    req2 = Mock()
    req2.headers = {}
    req2._cookies = Mock()
    
    # The header sent in second retry should have nc=00000002
    retry_req2 = Mock()
    retry_req2.headers = {}
    retry_req2.method = "GET"
    retry_req2.url = "http://a.com"
    req2.copy.return_value = retry_req2
    
    resp2 = Mock()
    resp2.status_code = 401
    # Server sends SAME nonce
    resp2.headers = {
        "www-authenticate": f'Digest realm="r", nonce="{nonce}", qop="auth"'
    }
    resp2.request = req2
    resp2.connection.send.return_value = Mock(history=[])
    
    with patch("requests.auth.extract_cookies_to_jar"):
        auth(req2) # Should verify preservation of state
        auth.handle_401(resp2)
        
    # Assert
    assert auth._thread_local.nonce_count == 2
    auth_header = retry_req2.headers["Authorization"]
    assert "nc=00000002" in auth_header

'''
Execution failed:

if i > 0 and url[0].isascii() and url[0].isalpha():
           ^^^^^
E       TypeError: '>' not supported between instances of 'Mock' and 'int'
'''