import pytest
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response
from unittest.mock import Mock, MagicMock

def test_digest_auth_extracts_cookies():
    """
    Test that cookies from the 401 response are extracted and added to the retried request.
    This requires a mock response structure compatible with extract_cookies_to_jar.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/")
    auth(req)
    
    resp = Response()
    resp.status_code = 401
    resp.request = req
    resp.headers["www-authenticate"] = 'Digest realm="r", nonce="n", qop="auth"'
    resp._content = b""
    
    # Mock connection
    mock_connection = Mock()
    resp.connection = mock_connection
    mock_connection.send.return_value = Response()
    
    # Mock internals for extract_cookies_to_jar
    # response.raw._original_response.msg
    mock_raw = Mock()
    mock_orig = Mock()
    mock_msg = MagicMock()
    
    # The 'msg' object is used by http.cookiejar. It typically calls msg.get_all("Set-Cookie", [])
    # or iter_items. requests.cookies.MockResponse delegates to it.
    # We simulate a Set-Cookie header.
    mock_msg.get_all.return_value = ["session=123; Path=/"]
    # Some implementations might check for info() or other methods, 
    # but MockResponse typically wraps headers.
    
    mock_orig.msg = mock_msg
    mock_raw._original_response = mock_orig
    resp.raw = mock_raw
    
    handle_401_hook = req.hooks["response"][0]
    handle_401_hook(resp)
    
    sent_request = mock_connection.send.call_args[0][0]
    
    # Verify Cookie header is present in the retried request
    assert "Cookie" in sent_request.headers
    assert "session=123" in sent_request.headers["Cookie"]