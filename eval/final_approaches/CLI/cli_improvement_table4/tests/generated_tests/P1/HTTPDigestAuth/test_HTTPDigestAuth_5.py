import pytest
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_HTTPDigestAuth_handle_401_no_digest():
    """Test handle_401 when response is not a digest challenge."""
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    resp = Mock()
    resp.status_code = 401
    resp.headers = {"www-authenticate": "Basic realm=foo"}
    
    # Should just return response without retrying
    result = auth.handle_401(resp)
    assert result == resp
    assert auth._thread_local.num_401_calls == 1
