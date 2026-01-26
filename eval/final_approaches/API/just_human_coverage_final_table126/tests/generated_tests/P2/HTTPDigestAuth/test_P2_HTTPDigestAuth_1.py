import threading
from requests.auth import HTTPDigestAuth

def test_build_digest_header_md5():
    # Scenario: Verify correct Authorization header generation for MD5 algorithm
    auth = HTTPDigestAuth("user", "pass")
    
    # Manually initialize thread local state to simulate an active authentication flow
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "me@kennethreitz.com",
        "nonce": "5a41c7b8d4c94446b4e4775d7422634a",
        "qop": "auth",
        "algorithm": "MD5",
        "opaque": "e645731725b74542617f168c13009778"
    }
    
    header = auth.build_digest_header("GET", "http://kennethreitz.com/digest-auth/auth/user/pass/MD5/never")
    
    # Assertions on the generated header string
    assert header.startswith("Digest ")
    assert 'username="user"' in header
    assert 'realm="me@kennethreitz.com"' in header
    assert 'nonce="5a41c7b8d4c94446b4e4775d7422634a"' in header
    assert 'uri="/digest-auth/auth/user/pass/MD5/never"' in header
    assert 'response="' in header
    assert 'algorithm="MD5"' in header
    assert 'opaque="e645731725b74542617f168c13009778"' in header
    assert 'qop="auth"' in header
    assert 'nc=00000001' in header
    assert 'cnonce="' in header