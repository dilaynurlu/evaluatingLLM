import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from requests.adapters import HTTPAdapter

def test_digest_auth_md5_happy_path():
    """
    Test the standard Digest Auth flow with default MD5 algorithm and qop='auth'.
    Verifies that handle_401 intercepts the 401 response, parses the challenge,
    and retries the request with a properly formatted Authorization header.
    """
    # Setup the auth object
    auth = HTTPDigestAuth("user", "pass")
    
    # Prepare a request
    url = "http://example.com/resource"
    req = PreparedRequest()
    req.prepare(method="GET", url=url)
    
    # Initialize auth state
    auth(req)
    
    # Create the 401 Response triggering the auth challenge
    r_401 = Response()
    r_401.status_code = 401
    r_401.reason = "Unauthorized"
    r_401.url = url
    r_401.request = req
    # Pre-populate content to avoid I/O
    r_401._content = b"Unauthorized"
    r_401._content_consumed = True
    
    # Challenge header
    nonce = "dcd98b7102dd2f0e8b11d0f600bfb0c093"
    realm = "testrealm@host.com"
    r_401.headers["www-authenticate"] = f'Digest realm="{realm}", nonce="{nonce}", qop="auth", opaque="5ccc069c403ebaf9f0171e9517f40e41"'
    
    # Mock the connection to intercept the retry
    adapter_mock = Mock(spec=HTTPAdapter)
    r_success = Response()
    r_success.status_code = 200
    r_success._content = b"Success"
    r_success._content_consumed = True
    r_success.history = []
    # The retry should return a success
    adapter_mock.send.return_value = r_success
    r_401.connection = adapter_mock
    
    # Trigger the hook
    result = auth.handle_401(r_401)
    
    # Verify the result is the success response
    assert result.status_code == 200
    
    # Verify send was called with a new prepared request
    assert adapter_mock.send.called
    args, _ = adapter_mock.send.call_args
    sent_request = args[0]
    
    # Check Authorization header presence and structure
    auth_header = sent_request.headers.get("Authorization")
    assert auth_header is not None
    assert auth_header.startswith("Digest ")
    
    # Verify key components of the digest header
    assert f'username="user"' in auth_header
    assert f'realm="{realm}"' in auth_header
    assert f'nonce="{nonce}"' in auth_header
    assert 'uri="/resource"' in auth_header
    assert 'response="' in auth_header
    assert 'qop="auth"' in auth_header
    assert 'nc=00000001' in auth_header
    assert 'cnonce="' in auth_header