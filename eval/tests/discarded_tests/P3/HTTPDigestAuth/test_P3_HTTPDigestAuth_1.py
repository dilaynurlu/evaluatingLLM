import hashlib
import re
from unittest.mock import Mock
import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_md5_success():
    """
    Test standard MD5 Digest Authentication flow with Unicode credentials.
    Verifies that handle_401 parses the challenge, generates the correct response,
    and resends the request with the Authorization header.
    Refined to use robust header parsing and unicode inputs.
    """
    # 1. Setup Request and Auth with Unicode to test encoding handling
    url = "http://example.org/resource"
    method = "GET"
    # Using characters that result in different bytes in UTF-8 vs Latin-1
    username = "us€r" 
    password = "p@sswørd"
    
    auth = HTTPDigestAuth(username, password)
    req = Request(method, url).prepare()
    
    # Initialize hooks and state
    auth(req)
    
    # 2. Setup 401 Response with MD5 challenge
    resp = Response()
    resp.request = req
    resp.status_code = 401
    nonce = "dcd98b7102dd2f0e8b11d0f600bfb0c093"
    realm = "testr€alm@host.com"
    opaque = "5ccc069c403ebaf9f0171e9517f40e41"
    
    # Challenge string
    challenge = f'Digest realm="{realm}", nonce="{nonce}", qop="auth", opaque="{opaque}"'
    resp.headers['www-authenticate'] = challenge
    
    # Mock internals
    resp._content = b"" 
    resp.raw = Mock()
    resp.raw._original_response = None 
    
    # Mock connection.send to capture the retried request
    mock_connection = Mock()
    mock_sent_response = Response()
    mock_sent_response.status_code = 200
    mock_sent_response.request = req 
    mock_sent_response.history = [] 
    mock_connection.send.return_value = mock_sent_response
    resp.connection = mock_connection
    
    # 3. Trigger handle_401
    result_response = auth.handle_401(resp)
    
    # 4. Verify the retry
    assert result_response.status_code == 200
    assert mock_connection.send.called
    
    # Get the prepared request that was sent
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers['Authorization']
    
    assert auth_header.startswith("Digest ")
    
    # Robust Regex Parsing of Authorization Header
    def get_auth_param(name, header):
        # matches key="value" or key=value, handling optional quotes and surrounding whitespace/commas
        pattern = re.compile(f'{name}=(?:"([^"]+)"|([^, ]+))')
        match = pattern.search(header)
        if match:
            return match.group(1) or match.group(2)
        return None

    assert get_auth_param('username', auth_header) == username
    assert get_auth_param('realm', auth_header) == realm
    assert get_auth_param('nonce', auth_header) == nonce
    assert get_auth_param('uri', auth_header) == "/resource"
    assert get_auth_param('opaque', auth_header) == opaque
    assert get_auth_param('algorithm', auth_header) == "MD5"
    assert get_auth_param('qop', auth_header) == "auth"
    assert get_auth_param('nc', auth_header) == "00000001"
    
    cnonce = get_auth_param('cnonce', auth_header)
    assert cnonce is not None
    # Verify cnonce is a hex string (common implementation)
    assert re.match(r'^[0-9a-fA-F]+$', cnonce)

    # Verify the hash response
    # Requests encodes to UTF-8 for calculation
    # HA1 = MD5(username:realm:password)
    a1 = f"{username}:{realm}:{password}"
    ha1 = hashlib.md5(a1.encode('utf-8')).hexdigest()
    
    # HA2 = MD5(method:digestURI)
    a2 = f"{method}:/resource"
    ha2 = hashlib.md5(a2.encode('utf-8')).hexdigest()
    
    # Response = MD5(HA1:nonce:nc:cnonce:qop:HA2)
    nc = "00000001"
    qop = "auth"
    response_data = f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}"
    expected_response = hashlib.md5(response_data.encode('utf-8')).hexdigest()
    
    assert get_auth_param('response', auth_header) == expected_response