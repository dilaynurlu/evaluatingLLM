import pytest
import re
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response
from requests.structures import CaseInsensitiveDict

def test_digest_auth_preemptive_nonce_reuse():
    """
    Test that if a nonce was established in a previous request,
    a subsequent request uses it preemptively.
    Refined to verify the Authorization header content specifically matches the stored nonce.
    """
    auth = HTTPDigestAuth("user", "pass")
    nonce_val = "saved_nonce"
    
    # Phase 1: Establish a nonce via a 401 flow
    req1 = Request("GET", "http://example.com/1").prepare()
    auth(req1)
    
    resp1 = Response()
    resp1.status_code = 401
    resp1.request = req1
    resp1.headers = CaseInsensitiveDict({
        "www-authenticate": f'Digest realm="realm", nonce="{nonce_val}", qop="auth"'
    })
    resp1.raw = Mock()
    resp1._content = b""
    resp1.connection = Mock()
    resp1.connection.send.return_value = Response()
    
    auth.handle_401(resp1)
    
    # Phase 2: Create a new request and apply auth
    # It should have Authorization header immediately because the nonce is cached
    req2 = Request("GET", "http://example.com/2").prepare()
    auth(req2)
    
    auth_header = req2.headers.get("Authorization")
    assert auth_header is not None
    assert auth_header.startswith("Digest ")
    
    # Verify the nonce used is the one from the previous 401
    match = re.search(r'nonce="([^"]+)"', auth_header)
    assert match is not None
    assert match.group(1) == nonce_val