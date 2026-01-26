import threading
from requests.auth import HTTPDigestAuth

def test_build_digest_header_with_query_params():
    # Scenario: Verify uri field includes query parameters
    auth = HTTPDigestAuth("user", "pass")
    
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "qop": "auth"
    }
    
    # URL with query string
    url = "http://example.com/search?q=test&page=1"
    header = auth.build_digest_header("GET", url)
    
    # The uri field in the header must contain path and query
    assert 'uri="/search?q=test&page=1"' in header