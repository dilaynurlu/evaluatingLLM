import pytest
import hashlib
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_md5_success():
    """
    Test the standard MD5 Digest Authentication flow.
    Verifies that a 401 response with MD5 challenge triggers a retry with
    the correct Authorization header structure and hash calculation.
    """
    username = "user"
    password = "password"
    realm = "testrealm"
    nonce = "dcd98b7102dd2f0e8b11d0f600bfb0c093"
    method = "GET"
    path = "/path"
    url = f"http://example.com{path}"
    
    # Pre-calculated values for assertions
    # HA1 = MD5(username:realm:password)
    ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode("utf-8")).hexdigest()
    # HA2 = MD5(method:uri)
    ha2 = hashlib.md5(f"{method}:{path}".encode("utf-8")).hexdigest()
    
    # We will control the cnonce and nonce_count for deterministic hash check
    fixed_cnonce = "0a4f113b"
    nc_value = "00000001"
    qop = "auth"
    
    # Expected Response = MD5(HA1:nonce:nc:cnonce:qop:HA2)
    expected_response_hash = hashlib.md5(
        f"{ha1}:{nonce}:{nc_value}:{fixed_cnonce}:{qop}:{ha2}".encode("utf-8")
    ).hexdigest()

    auth = HTTPDigestAuth(username, password)
    
    # Prepare the initial request
    request = Request(method, url).prepare()
    
    # Initialize auth state on the request
    auth(request)

    # Mock the 401 Response
    response_401 = Response()
    response_401.status_code = 401
    response_401.request = request
    response_401.url = url
    response_401.reason = "Unauthorized"
    response_401.headers["www-authenticate"] = f'Digest realm="{realm}", nonce="{nonce}", qop="{qop}", algorithm="MD5"'
    response_401._content = b"" # Avoid I/O
    response_401.raw = Mock() # Mock raw to avoid cookie extraction failure

    # Mock connection.send to capture the retry request
    mock_connection = Mock()
    response_401.connection = mock_connection
    
    mock_sent_response = Response()
    mock_sent_response.status_code = 200
    mock_sent_response.history = [] # Must differ from original to show history append
    mock_sent_response.request = Mock()
    mock_connection.send.return_value = mock_sent_response

    # Patch os.urandom and time.ctime to control cnonce generation
    # The code generates cnonce via: hashlib.sha1(nonce_count + nonce + time + urandom).hexdigest()[:16]
    # We can't easily predict the input to sha1 without mocking everything, 
    # but we can mock the hashlib.sha1 result or the random sources.
    # Actually, simpler: patch hashlib.sha1 to return a mock that produces our fixed_cnonce
    # But hashlib is used for HA1/HA2 too. 
    # Better strategy: Patch the random parts and let logic run, or inspect the header structure without validating the exact hash bits 
    # if mocking is too complex. 
    # However, to be "complete", let's use a side_effect on hashlib.sha1 OR simply allow the code to run 
    # and capture the cnonce from the header, then verify the response hash matches that cnonce.
    
    # Let's perform the verification by capturing the generated header
    # and re-calculating the hash using the cnonce found in that header.
    
    final_response = auth.handle_401(response_401)
    
    assert final_response.status_code == 200
    assert mock_connection.send.call_count == 1
    
    retry_request = mock_connection.send.call_args[0][0]
    auth_header = retry_request.headers["Authorization"]
    
    # Parse the generated Authorization header
    assert auth_header.startswith("Digest ")
    parts = {}
    for part in auth_header[7:].split(", "):
        key, val = part.split("=", 1)
        val = val.strip('"')
        parts[key] = val
        
    assert parts["username"] == username
    assert parts["realm"] == realm
    assert parts["nonce"] == nonce
    assert parts["uri"] == path
    assert parts["algorithm"] == "MD5"
    assert parts["qop"] == "auth"
    assert parts["nc"] == "00000001"
    
    # Now verify the cryptographic response using the cnonce actually generated
    generated_cnonce = parts["cnonce"]
    
    recalc_response = hashlib.md5(
        f"{ha1}:{nonce}:{nc_value}:{generated_cnonce}:{qop}:{ha2}".encode("utf-8")
    ).hexdigest()
    
    assert parts["response"] == recalc_response