import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_build_digest_header_md5():
    """Test building digest header with MD5 default."""
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    # Setup challenge
    auth._thread_local.chal = {
        "realm": "me@kennethreitz.com",
        "nonce": "e966c9325530953c080014a400000001",
        "qop": "auth"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/foo")
    assert header.startswith("Digest ")
    assert 'username="user"' in header
    assert 'realm="me@kennethreitz.com"' in header
    assert 'nonce="e966c9325530953c080014a400000001"' in header
    assert 'algorithm="MD5"' not in header # Default MD5 is implied if not present? 
    # Wait, code: if algorithm is None: _algorithm="MD5". 
    # output: if algorithm: base += ... 
    # So if chal doesn't have algorithm, it uses MD5 for calc but doesn't put it in header?
    # Actually checking code: "if algorithm is None: _algorithm = 'MD5' ... if algorithm: base += ..."
    # Yes.
