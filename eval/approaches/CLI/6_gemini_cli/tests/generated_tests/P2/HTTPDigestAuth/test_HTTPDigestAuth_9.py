import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_unknown_algorithm():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "algorithm": "UNKNOWN"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/")
    # If algorithm unknown, hash_utf8 remains None -> returns None
    assert header is None
