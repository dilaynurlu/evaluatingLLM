import pytest
from unittest.mock import MagicMock
from requests.auth import HTTPDigestAuth
from requests.models import Response

def test_HTTPDigestAuth_handle_401_no_digest_in_header():
    """
    Test that handle_401 returns original response if no 'Digest' in header.
    """
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    # Mock Response with Basic Auth
    r = MagicMock(spec=Response)
    r.status_code = 401
    r.headers = {
        "www-authenticate": 'Basic realm="testrealm"'
    }
    r.request = MagicMock()
    r.connection = MagicMock()
    
    # Call handle_401
    result = auth.handle_401(r)
    
    # Should return original response
    assert result == r
    # Should not have called connection.send
    assert not r.connection.send.called
