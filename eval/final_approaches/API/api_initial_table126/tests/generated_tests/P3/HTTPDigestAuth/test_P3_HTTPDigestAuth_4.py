import re
from unittest.mock import Mock
import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_reuses_nonce():
    """
    Test that HTTPDigestAuth reuses the negotiated nonce on subsequent requests
    and increments the nonce count (nc).
    Refined with robust parsing.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Helper for parsing
    def get_auth_param(name, header):
        pattern = re.compile(f'{name}=(?:"([^"]+)"|([^, ]+))')
        match = pattern.search(header)
        if match:
            return match.group(1) or match.group(2)
        return None

    # 1. First Request: Triggers the 401 challenge flow
    req1 = Request('GET', 'http://site.com/1').prepare()
    auth(req1)
    
    resp1 = Response()
    resp1.request = req1
    resp1.status_code = 401
    resp1.headers['www-authenticate'] = 'Digest realm="r", nonce="shared_nonce", qop="auth"'
    resp1._content = b""
    resp1.raw = Mock()
    resp1.raw._original_response = None
    
    mock_conn = Mock()
    mock_conn.send.return_value = Response()
    mock_conn.send.return_value.status_code = 200
    mock_conn.send.return_value.history = []
    resp1.connection = mock_conn
    
    # This establishes the session state (nonce, realm, etc.)
    auth.handle_401(resp1)
    
    # Verify first retry used nc=1
    first_retry = mock_conn.send.call_args[0][0]
    assert get_auth_param('nc', first_retry.headers['Authorization']) == '00000001'
    
    # 2. Second Request: Should use stored nonce PREEMPTIVELY without 401
    req2 = Request('GET', 'http://site.com/2').prepare()
    
    # Calling auth(req2) should immediately attach Authorization header
    # because 'last_nonce' is set in thread local storage.
    auth(req2)
    
    assert 'Authorization' in req2.headers
    header = req2.headers['Authorization']
    
    assert get_auth_param('nonce', header) == "shared_nonce"
    assert get_auth_param('uri', header) == "/2"
    
    # Verify nonce count incremented to 2
    assert get_auth_param('nc', header) == '00000002'