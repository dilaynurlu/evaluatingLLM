import pytest
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_HTTPDigestAuth_handle_401_ignore_no_digest_header():
    auth = HTTPDigestAuth("user", "pass")
    
    r = Mock()
    r.status_code = 401
    r.headers = {"www-authenticate": 'Basic realm="realm"'} # Not Digest
    
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 1
    
    result = auth.handle_401(r)
    
    assert result == r
