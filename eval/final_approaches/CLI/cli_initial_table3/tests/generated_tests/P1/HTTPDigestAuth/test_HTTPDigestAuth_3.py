import io
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response
from unittest.mock import MagicMock, patch

def test_HTTPDigestAuth_md5_challenge():
    auth = HTTPDigestAuth("user", "passwd")
    
    # Mock Response with 401
    r = Response()
    r.status_code = 401
    r.url = "http://example.com/foo"
    r.headers = {"www-authenticate": 'Digest realm="testrealm", nonce="12345", algorithm="MD5", qop="auth"'}
    r.raw = io.BytesIO(b"")
    r.reason = "Unauthorized"
    r.encoding = "utf-8"
    
    # Mock request associated with response
    req = Request('GET', 'http://example.com/foo')
    r.request = req.prepare()
    r.request.body = None 
    
    # Mock connection and sending a new request
    r.connection = MagicMock()
    
    # Mock send to return a new Response (success)
    success_response = Response()
    success_response.status_code = 200
    success_response.request = r.request.copy() # Just to have something
    success_response.history = []
    r.connection.send.return_value = success_response
    
    # We need to ensure `auth` has initialized thread local state.
    # We can do this by calling it on the request first.
    auth(r.request) 
    
    # Mock extract_cookies_to_jar to do nothing
    with patch('requests.auth.extract_cookies_to_jar'):
        # Call handle_401
        result = auth.handle_401(r)
    
    # Verify a new request was sent
    assert r.connection.send.called
    
    # Verify Authorization header in the new request
    args, _ = r.connection.send.call_args
    new_request = args[0]
    
    auth_header = new_request.headers['Authorization']
    assert auth_header.startswith("Digest ")
    assert 'username="user"' in auth_header
    assert 'realm="testrealm"' in auth_header
    assert 'nonce="12345"' in auth_header
    assert 'algorithm="MD5"' in auth_header
    assert 'response="' in auth_header
    assert 'uri="/foo"' in auth_header