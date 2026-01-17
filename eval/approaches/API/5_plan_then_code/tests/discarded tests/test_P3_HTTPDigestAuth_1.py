import hashlib
import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_md5_success():
    """
    Test standard MD5 Digest Authentication flow using a Known Answer Test (KAT) approach.
    Inputs are fixed to ensure deterministic output, verifying against a pre-calculated hash.
    """
    # KAT Inputs
    username = "u"
    password = "p"
    realm = "r"
    nonce = "n"
    method = "GET"
    uri = "/path"
    opaque = "o"
    # Fixed mocks for cnonce generation
    # requests logic: s = str(nonce_count) + nonce + time + urandom
    # We mock time.ctime() and os.urandom() to control this.
    fixed_time = "t"
    fixed_salt = b"s"
    
    # Pre-calculated Expectation:
    # 1. cnonce calculation:
    #    s = "1" + "n" + "t" + "s" => b"1nts"
    #    cnonce = hashlib.sha1(b"1nts").hexdigest()[:16]
    #    sha1("1nts") = 03de6c570bfe24bfc328ccd7cae8b7cc6b75f798
    #    cnonce = "03de6c570bfe24bf"
    #
    # 2. HA1 = MD5("u:r:p")
    #    MD5("u:r:p") = 4b68ab3847feda7d6c62c1fbcbe8bdc7
    #
    # 3. HA2 = MD5("GET:/path")
    #    MD5("GET:/path") = 392949021a8d01193aac1e5df9877b0d
    #
    # 4. Response = MD5(HA1:nonce:nc:cnonce:qop:HA2)
    #    Str: "4b68ab3847feda7d6c62c1fbcbe8bdc7:n:00000001:03de6c570bfe24bf:auth:392949021a8d01193aac1e5df9877b0d"
    #    MD5(...) = 16007e2c909678c187313835e589bf00
    
    expected_response = "16007e2c909678c187313835e589bf00"
    expected_cnonce = "03de6c570bfe24bf"
    
    auth = HTTPDigestAuth(username, password)
    req = Request(method, f"http://example.com{uri}").prepare()
    auth(req)
    
    response = Response()
    response.status_code = 401
    response.request = req
    response.url = f"http://example.com{uri}"
    response._content = b""
    response.headers["www-authenticate"] = f'Digest realm="{realm}", nonce="{nonce}", qop="auth", opaque="{opaque}", algorithm="MD5"'
    
    response.connection = Mock()
    response.connection.send.return_value = Response()
    
    with patch("os.urandom", return_value=fixed_salt), \
         patch("time.ctime", return_value=fixed_time):
        auth.handle_401(response)
    
    assert response.connection.send.call_count == 1
    sent_request = response.connection.send.call_args[0][0]
    auth_header = sent_request.headers["Authorization"]
    
    # Parse header to dict for robust assertion
    assert auth_header.startswith("Digest ")
    parts = auth_header[7:].split(", ")
    header_dict = {}
    for part in parts:
        if "=" in part:
            k, v = part.split("=", 1)
            header_dict[k] = v.strip('"')
            
    assert header_dict['username'] == username
    assert header_dict['realm'] == realm
    assert header_dict['nonce'] == nonce
    assert header_dict['uri'] == uri
    assert header_dict['opaque'] == opaque
    assert header_dict['qop'] == 'auth'
    assert header_dict['nc'] == '00000001'
    assert header_dict['cnonce'] == expected_cnonce
    assert header_dict['response'] == expected_response
    assert header_dict['algorithm'] == 'MD5'