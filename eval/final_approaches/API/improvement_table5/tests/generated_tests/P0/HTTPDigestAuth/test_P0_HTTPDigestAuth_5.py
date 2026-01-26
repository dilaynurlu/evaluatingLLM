import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_nonce_count_increment():
    """
    Test that consecutive 401 responses with the same nonce 
    cause the nonce count (nc) to increment.
    """
    username = "user"
    password = "password"
    nonce = "persistent-nonce"
    
    auth = HTTPDigestAuth(username, password)
    request = Request("GET", "http://example.com/").prepare()
    auth(request) # Init state

    # First Challenge
    r1 = Response()
    r1.status_code = 401
    r1.request = request
    r1.url = "http://example.com/"
    r1.headers["www-authenticate"] = f'Digest realm="test", nonce="{nonce}", qop="auth"'
    r1._content = b""
    r1.raw = Mock()
    r1.connection = Mock()
    r1.connection.send.return_value = Response() # Success ignored here

    auth.handle_401(r1)
    
    req1 = r1.connection.send.call_args[0][0]
    auth_header1 = req1.headers["Authorization"]
    assert "nc=00000001" in auth_header1

    # Second Challenge: Same nonce (simulate auth failure or subsequent request with same nonce)
    # Important: In handle_401, state is stored in thread_local. 
    # To test increment, we call handle_401 again.
    
    r2 = Response()
    r2.status_code = 401
    r2.request = request
    r2.url = "http://example.com/"
    r2.headers["www-authenticate"] = f'Digest realm="test", nonce="{nonce}", qop="auth"'
    r2._content = b""
    r2.raw = Mock()
    r2.connection = Mock()
    r2.connection.send.return_value = Response()

    # Reset num_401_calls to allow processing again (simulate new request in session)
    # But strictly, handle_401 increments num_401_calls. 
    # The nonce count logic is inside build_digest_header.
    # To properly simulate a sequence where nonce is reused, we need to ensure handle_401 
    # proceeds. If num_401_calls >= 2, it stops.
    # We manually reset the loop counter for this test to focus on nonce counting, 
    # simulating a fresh request that happened to get the same nonce from server.
    auth._thread_local.num_401_calls = 1

    auth.handle_401(r2)
    
    req2 = r2.connection.send.call_args[0][0]
    auth_header2 = req2.headers["Authorization"]
    assert "nc=00000002" in auth_header2
    
    # Third Challenge: Different nonce (Should reset nc)
    new_nonce = "new-nonce"
    r3 = Response()
    r3.status_code = 401
    r3.request = request
    r3.url = "http://example.com/"
    r3.headers["www-authenticate"] = f'Digest realm="test", nonce="{new_nonce}", qop="auth"'
    r3._content = b""
    r3.raw = Mock()
    r3.connection = Mock()
    r3.connection.send.return_value = Response()
    
    auth._thread_local.num_401_calls = 1
    auth.handle_401(r3)
    
    req3 = r3.connection.send.call_args[0][0]
    auth_header3 = req3.headers["Authorization"]
    assert "nc=00000001" in auth_header3
    assert f'nonce="{new_nonce}"' in auth_header3