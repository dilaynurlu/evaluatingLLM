import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Response

def test_HTTPDigestAuth_handle_401_no_digest_header():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    r = Response()
    r.status_code = 401
    r.headers = {"www-authenticate": 'Basic realm="me@test.com"'} # Not digest
    r.request = Mock(spec=PreparedRequest)
    r.request.body = Mock()
    
    # Mock body.seek to avoid attribute error if checked
    r.request.body.seek = Mock()
    
    # Mock thread local pos
    auth._thread_local.pos = 0
    
    result = auth.handle_401(r)
    
    assert result == r
    # Should reset num_401_calls to 1
    assert auth._thread_local.num_401_calls == 1

from unittest.mock import Mock
from requests.models import PreparedRequest
