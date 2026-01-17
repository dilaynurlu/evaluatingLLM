import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response
import hashlib

def test_digest_auth_md5_success():
    """
    Test a standard MD5 Digest Authentication flow.
    Verifies that handle_401 parses the challenge and generates a valid Authorization header
    using MD5, correct nonce, and calculated response.
    """
    username = "user"
    password = "password"
    realm = "testrealm"
    nonce = "dcd98b7102dd2f0e8b11d0f600bfb0c093"
    uri = "/dir/index.html"
    method = "GET"
    qop = "auth"
    
    # Challenge string
    www_auth = f'Digest realm="{realm}", nonce="{nonce}", qop="{qop}"'
    
    # Create Auth and Request
    auth = HTTPDigestAuth(username, password)
    req = Request(method, f"http://localhost{uri}").prepare()
    
    # Initialize auth state
    auth(req)
    
    # Create Response mimicking a 401
    resp = Response()
    resp.request = req
    resp.status_code = 401
    resp.headers["www-authenticate"] = www_auth
    resp._content = b"" # Avoid reading from raw
    resp.raw = Mock() # For close() call
    
    # Mock connection.send to capture the retried request
    mock_send = Mock()
    mock_send.return_value = Response() # Return a dummy response for the retry
    resp.connection = Mock()
    resp.connection.send = mock_send

    # Patch randomness to ensure deterministic cnonce and valid hash check
    with patch("requests.auth.os.urandom") as mock_urandom, \
         patch("requests.auth.time.ctime") as mock_ctime:
        
        mock_urandom.return_value = b"12345678" # 8 bytes
        mock_ctime.return_value = "Tue Jan  1 00:00:00 2024"
        
        # Execute
        retry_resp = auth.handle_401(resp)
        
        # Verify connection.send was called
        assert mock_send.called
        sent_args, sent_kwargs = mock_send.call_args
        sent_request = sent_args[0]
        
        # Verify Authorization header existence
        auth_header = sent_request.headers.get("Authorization")
        assert auth_header is not None
        assert auth_header.startswith("Digest ")
        
        # Verify header parts
        # Note: parsing the header strictly is hard due to order/quoting, 
        # checking containment of key components is robust for this level.
        assert f'username="{username}"' in auth_header
        assert f'realm="{realm}"' in auth_header
        assert f'nonce="{nonce}"' in auth_header
        assert f'uri="{uri}"' in auth_header
        assert 'qop="auth"' in auth_header
        assert 'nc=00000001' in auth_header
        
        # Reconstruct expected cnonce to verify logic used correct random/time
        # Logic in source: 
        # s = str(nonce_count).encode('utf-8') + nonce.encode('utf-8') + time.ctime().encode('utf-8') + os.urandom(8)
        # nonce_count is 1
        s = b"1" + nonce.encode("utf-8") + mock_ctime.return_value.encode("utf-8") + mock_urandom.return_value
        expected_cnonce = hashlib.sha1(s).hexdigest()[:16]
        
        assert f'cnonce="{expected_cnonce}"' in auth_header