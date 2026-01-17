import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_digest_auth_success_md5_qop_auth():
    """
    Test standard MD5 Digest Auth with qop="auth".
    Verifies that a 401 response with a valid challenge triggers a new request
    with the correct Authorization header structure.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Create the original request
    request = PreparedRequest()
    request.prepare(
        method="GET",
        url="http://example.com/resource",
        headers={"Host": "example.com"}
    )
    
    # Initialize auth state on the request
    auth(request)
    
    # Create the 401 response with digest challenge
    response = Response()
    response.status_code = 401
    response.request = request
    response.headers["www-authenticate"] = 'Digest realm="testrealm", nonce="dcd98b7102dd2f0e8b11d0f600bfb0c093", qop="auth", opaque="5ccc069c403ebaf9f0171e9517f40e41"'
    response._content = b""  # Avoid raw read
    response.raw = Mock()    # Avoid cookie extraction errors
    del response.raw._original_response # Ensure extract_cookies_to_jar returns early

    # Mock the connection to intercept the retried request
    response.connection = Mock()
    mock_sent_response = Response()
    mock_sent_response.history = [] 
    response.connection.send.return_value = mock_sent_response

    # Execute handle_401
    result = auth.handle_401(response)

    # Assertions
    assert response.connection.send.called
    
    # Verify the sent request's Authorization header
    args, kwargs = response.connection.send.call_args
    sent_request = args[0]
    auth_header = sent_request.headers["Authorization"]
    
    assert auth_header.startswith("Digest ")
    assert 'username="user"' in auth_header
    assert 'realm="testrealm"' in auth_header
    assert 'nonce="dcd98b7102dd2f0e8b11d0f600bfb0c093"' in auth_header
    assert 'uri="/resource"' in auth_header
    assert 'qop="auth"' in auth_header
    assert 'nc=00000001' in auth_header
    assert 'cnonce="' in auth_header
    assert 'opaque="5ccc069c403ebaf9f0171e9517f40e41"' in auth_header
    assert 'response="' in auth_header
    
    # Since algorithm is implicit MD5, it might not be explicitly present if not in challenge,
    # or it might be present if the code adds it. The code adds it if it's in the challenge.
    # Here it wasn't in the challenge, so it should be absent or default.
    # Code: "if algorithm: base += ..." -> algorithm comes from chal.get("algorithm").
    # If not in chal, it is None (though _algorithm defaults to MD5 for calc).
    # So 'algorithm=' should NOT be in the header string if not in challenge.
    assert "algorithm=" not in auth_header