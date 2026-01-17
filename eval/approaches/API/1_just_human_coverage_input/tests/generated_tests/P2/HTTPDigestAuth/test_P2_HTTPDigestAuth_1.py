import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests import Request, Response

def test_digest_auth_md5_success_flow():
    """
    Test standard MD5 Digest Authentication flow with qop="auth".
    Verifies that the handle_401 hook correctly parses the challenge,
    generates the Authorization header including all required fields,
    and retries the request.
    """
    # 1. Setup Auth and Request
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.org/resource").prepare()
    
    # Initialize per-thread state by calling the auth object with the request
    auth(req)
    
    # 2. Create the 401 Response with a Digest challenge
    response = Response()
    response.status_code = 401
    response.url = "http://example.org/resource"
    response.request = req
    response.headers["www-authenticate"] = (
        'Digest realm="testrealm", nonce="12345", qop="auth", algorithm="MD5"'
    )
    # Ensure content consumption doesn't fail
    response._content = b""
    # Mock raw to support close() calls
    response.raw = Mock()
    
    # 3. Mock the connection to intercept the retry
    mock_connection = Mock()
    response.connection = mock_connection
    
    # The retry should succeed
    success_response = Response()
    success_response.status_code = 200
    mock_connection.send.return_value = success_response
    
    # 4. Trigger the 401 handler
    result = auth.handle_401(response)
    
    # 5. Assertions
    assert result.status_code == 200
    assert mock_connection.send.called
    
    # Inspect the prepared request sent in the retry
    retry_args = mock_connection.send.call_args
    sent_request = retry_args[0][0]
    
    auth_header = sent_request.headers.get("Authorization")
    assert auth_header is not None
    assert auth_header.startswith("Digest ")
    
    # Verify presence of components
    assert 'username="user"' in auth_header
    assert 'realm="testrealm"' in auth_header
    assert 'nonce="12345"' in auth_header
    assert 'uri="/resource"' in auth_header
    assert 'algorithm="MD5"' in auth_header
    assert 'qop="auth"' in auth_header
    assert 'cnonce="' in auth_header
    assert 'response="' in auth_header
    assert 'nc=00000001' in auth_header