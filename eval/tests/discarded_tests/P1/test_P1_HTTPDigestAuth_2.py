import pytest
from unittest.mock import MagicMock, patch
from requests.auth import HTTPDigestAuth
import requests

def test_digest_auth_handle_401_sha256_algorithm():
    """
    Test Digest Auth with SHA-256 algorithm specified in the challenge.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    initial_request = MagicMock(spec=requests.PreparedRequest)
    initial_request.method = "GET"
    initial_request.url = "http://example.org/path?query=1"
    initial_request.headers = {}
    initial_request.body = None
    initial_request.register_hook = MagicMock()
    
    auth(initial_request)
    
    r_401 = MagicMock(spec=requests.Response)
    r_401.request = initial_request
    
    new_request = MagicMock(spec=requests.PreparedRequest)
    new_request.headers = {}
    new_request.method = "GET"
    new_request.url = "http://example.org/path?query=1"
    new_request._cookies = MagicMock()
    new_request.prepare_cookies = MagicMock()
    initial_request.copy.return_value = new_request
    
    # SHA-256 challenge
    r_401.headers = {
        "www-authenticate": 'Digest realm="testrealm", nonce="testnonce", algorithm="SHA-256", qop="auth"'
    }
    r_401.status_code = 401
    r_401.is_redirect = False
    r_401.content = b""
    r_401.raw = MagicMock()
    
    r_401.connection = MagicMock()
    r_401.connection.send.return_value = MagicMock(spec=requests.Response)
    
    with patch("requests.auth.time") as mock_time, \
         patch("requests.auth.os") as mock_os, \
         patch("requests.auth.extract_cookies_to_jar"):
             
        mock_time.ctime.return_value = "fixed_time"
        mock_os.urandom.return_value = b"fixed_random"
        
        auth.handle_401(r_401)
        
        auth_header = new_request.headers.get("Authorization")
        assert 'algorithm="SHA-256"' in auth_header
        
        # Verify response length (SHA-256 hex digest is 64 chars)
        # Extract response value
        import re
        match = re.search(r'response="([^"]+)"', auth_header)
        assert match
        response_digest = match.group(1)
        assert len(response_digest) == 64


'''
Execution failed:

auth.handle_401(r_401)

eval/tests/generated_tests/P1/HTTPDigestAuth/test_P1_HTTPDigestAuth_2.py:51: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
requests/src/requests/auth.py:277: in handle_401
    _r.history.append(r)
    ^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <MagicMock name='mock.connection.send()' spec='Response' id='281472994798160'>
name = 'history'

    def __getattr__(self, name):
        if name in {'_mock_methods', '_mock_unsafe'}:
            raise AttributeError(name)
        elif self._mock_methods is not None:
            if name not in self._mock_methods or name in _all_magics:
>               raise AttributeError("Mock object has no attribute %r" % name)
E               AttributeError: Mock object has no attribute 'history'

/usr/local/lib/python3.11/unittest/mock.py:653: AttributeError
'''