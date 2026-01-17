import pytest
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_HTTPDigestAuth_limit_401_calls():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 2 # Limit is 2
    
    r = Mock()
    r.status_code = 401
    r.headers = {"www-authenticate": 'Digest realm="realm", nonce="nonce"'}
    
    result = auth.handle_401(r)
    
    assert result == r # Should give up
    assert auth._thread_local.num_401_calls == 1 # Should reset
