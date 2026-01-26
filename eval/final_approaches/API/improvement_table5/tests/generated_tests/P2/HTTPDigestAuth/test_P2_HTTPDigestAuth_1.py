import pytest
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response
from unittest.mock import Mock

def test_digest_auth_md5_default_qop_auth():
    """
    Test standard MD5 Digest Auth with qop="auth".
    Verifies that the Authorization header is correctly generated and attached
    to the retried request.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # 1. Prepare a request
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/resource")
    
    # 2. Attach auth (initializes state, registers hooks)
    auth(req)
    
    # 3. Create a 401 Response with Digest challenge
    resp = Response()
    resp.status_code = 401
    resp.request = req
    resp.headers["www-authenticate"] = (
        'Digest realm="testrealm", nonce="dcd98b7102dd2f0e8b11d0f600bfb0c093", '
        'qop="auth", opaque="5ccc069c403ebaf9f0171e9517f40e41"'
    )
    resp._content = b""  # Empty content
    
    # 4. Mock the connection to intercept the retry
    mock_connection = Mock()
    resp.connection = mock_connection
    
    # Mock the response of the retried request
    retry_resp = Response()
    retry_resp.status_code = 200
    mock_connection.send.return_value = retry_resp
    
    # 5. Trigger the handle_401 hook
    # Find the hook registered by auth
    handle_401_hook = None
    for hook in req.hooks["response"]:
        if getattr(hook, "__name__", "") == "handle_401":
            handle_401_hook = hook
            break
            
    assert handle_401_hook is not None
    
    # Execute hook
    final_resp = handle_401_hook(resp)
    
    # 6. Assertions
    # Ensure a new request was sent
    assert mock_connection.send.called
    assert final_resp == retry_resp
    
    # Inspect the request sent
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers.get("Authorization")
    
    assert auth_header is not None
    assert auth_header.startswith("Digest ")
    
    # Verify components of the Digest header
    assert 'username="user"' in auth_header
    assert 'realm="testrealm"' in auth_header
    assert 'nonce="dcd98b7102dd2f0e8b11d0f600bfb0c093"' in auth_header
    assert 'uri="/resource"' in auth_header
    assert 'qop="auth"' in auth_header
    assert 'nc=00000001' in auth_header
    assert 'cnonce="' in auth_header
    assert 'opaque="5ccc069c403ebaf9f0171e9517f40e41"' in auth_header
    # "response" is a hash, just check existence
    assert 'response="' in auth_header