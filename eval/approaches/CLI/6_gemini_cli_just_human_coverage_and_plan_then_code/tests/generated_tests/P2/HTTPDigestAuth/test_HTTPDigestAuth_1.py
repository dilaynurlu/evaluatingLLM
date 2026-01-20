import pytest
from requests.auth import HTTPDigestAuth
import threading

def test_HTTPDigestAuth_MD5_basic():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    # Mock challenge
    auth._thread_local.chal = {
        "realm": "me@kennethreitz.com",
        "nonce": "4d0479793910931e5f8f870530722168",
        "qop": "auth",
        "algorithm": "MD5"
    }
    
    # Expected HA1 = MD5(user:realm:pass)
    # Expected HA2 = MD5(GET:/path)
    # Response = MD5(HA1:nonce:nc:cnonce:qop:HA2)
    
    # Since cnonce is random, we can't predict exact string unless we mock os.urandom or time.
    # But we can verify structure.
    
    header = auth.build_digest_header("GET", "http://example.com/path")
    assert header.startswith("Digest ")
    assert 'username="user"' in header
    assert 'realm="me@kennethreitz.com"' in header
    assert 'nonce="4d0479793910931e5f8f870530722168"' in header
    assert 'uri="/path"' in header
    assert 'algorithm="MD5"' in header
    assert 'qop="auth"' in header
