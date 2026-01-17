import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_query_string():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "qop": "auth"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/path?query=1")
    assert 'uri="/path?query=1"' in header
