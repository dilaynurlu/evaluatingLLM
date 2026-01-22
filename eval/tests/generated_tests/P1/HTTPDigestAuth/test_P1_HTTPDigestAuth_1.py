import pytest
from requests.auth import HTTPDigestAuth
from requests import Request, Response
from unittest.mock import Mock

def test_digest_auth_md5_success():
    """
    Test the standard MD5 Digest Authentication flow.
    Verifies that a 401 response with a Digest challenge triggers the generation
    of a correct Authorization header using MD5 (default) and qop=auth.
    """
    url = "http://example.org/resource"
    auth = HTTPDigestAuth("user", "pass")
    
    # Create a prepared request
    # usage of .prepare() ensures we have a valid PreparedRequest
    req = Request("GET", url).prepare()
    
    # Initialize the auth hook (sets up thread local state)
    auth(req)
    
    # Simulate a 401 Response with a Digest challenge
    resp = Response()
    resp.status_code = 401
    resp.headers["www-authenticate"] = 'Digest realm="myrealm", nonce="mynonce", qop="auth", opaque="myopaque"'
    resp.url = url
    resp.request = req
    resp._content = b""  # Bypass reading from raw
    
    # Mock the connection to intercept the re-sent request
    resp.raw = Mock()
    resp.connection = Mock()
    
    # The resent request should receive a 200 OK
    success_resp = Response()
    success_resp.status_code = 200
    success_resp._content = b"success"
    success_resp.history = [] 
    success_resp.request = None 
    
    resp.connection.send.return_value = success_resp

    # Trigger handle_401
    result = auth.handle_401(resp)
    
    # Verify the result is the success response
    assert result.status_code == 200
    
    # Verify connection.send was called exactly once (the retry)
    assert resp.connection.send.call_count == 1
    
    # Verify the Authorization header in the retry
    sent_request = resp.connection.send.call_args[0][0]
    auth_header = sent_request.headers.get("Authorization")
    
    assert auth_header is not None
    assert auth_header.startswith("Digest ")
    
    # Check components of the header
    # Order is not strictly guaranteed by dict, but logic constructs string in specific order or appended.
    # We check for presence of correct substrings.
    expected_parts = [
        'username="user"',
        'realm="myrealm"',
        'nonce="mynonce"',
        'uri="/resource"',
        'response=',
        'qop="auth"',
        'nc=00000001',
        'opaque="myopaque"'
    ]
    
    for part in expected_parts:
        assert part in auth_header, f"Missing {part} in {auth_header}"
    
    # cnonce should be present and random
    assert 'cnonce="' in auth_header