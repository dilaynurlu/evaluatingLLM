import pytest
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_HTTPDigestAuth_handle_401_too_many_retries():
    """Test handle_401 aborts if too many retries."""
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 2 # Limit is 2
    
    resp = Mock()
    resp.status_code = 401
    resp.headers = {"www-authenticate": 'Digest realm="test"'}
    
    result = auth.handle_401(resp)
    assert result == resp # Should return original response, not retry
    assert auth._thread_local.num_401_calls == 1 # Resets to 1? Code says: self._thread_local.num_401_calls = 1 return r
