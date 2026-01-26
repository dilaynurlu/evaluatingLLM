import pytest
import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_digest_auth_no_qop():
    """
    Test Digest Authentication when the server does not provide 'qop'.
    In this case, 'nc' (nonce count) and 'cnonce' (client nonce) should NOT be present.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    request = requests.Request("GET", "http://example.com/legacy").prepare()
    
    response_401 = requests.Response()
    response_401.status_code = 401
    # No qop parameter in the challenge
    response_401.headers["www-authenticate"] = (
        'Digest realm="LegacyRealm", nonce="legacynonce", algorithm="MD5"'
    )
    response_401.request = request
    response_401._content = b""
    response_401.raw = Mock()
    
    mock_connection = Mock()
    mock_connection.send.return_value = requests.Response()
    mock_connection.send.return_value.history = []
    mock_connection.send.return_value.request = requests.PreparedRequest()
    response_401.connection = mock_connection
    
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 1
    
    auth.handle_401(response_401)
    
    sent_req = mock_connection.send.call_args[0][0]
    auth_header = sent_req.headers["Authorization"]
    
    assert 'nonce="legacynonce"' in auth_header
    # 'qop', 'nc', and 'cnonce' must be absent if qop is not provided by server
    assert 'qop=' not in auth_header
    assert 'nc=' not in auth_header
    assert 'cnonce=' not in auth_header
    assert 'response="' in auth_header