import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session
from requests.models import Response, Request

def test_resolve_redirects_extracts_cookies():
    """
    Test that cookies set in the redirect response are extracted to the jar.
    Uses patching to verify extraction logic is invoked without relying on 
    brittle mocks of the raw response object.
    """
    session = Session()
    
    req = Request(method="GET", url="http://example.com/login").prepare()
    
    resp = Response()
    resp.status_code = 302
    resp.headers["Location"] = "/dashboard"
    resp.url = "http://example.com/login"
    resp._content = b""
    resp._content_consumed = True
    resp.request = req
    
    # Ensure resp.raw exists as it is passed to extract_cookies_to_jar
    resp.raw = Mock() 
    
    resp_next = Response()
    resp_next.status_code = 200
    resp_next._content = b""
    resp_next._content_consumed = True
    
    session.send = Mock(return_value=resp_next)
    
    # Patch extract_cookies_to_jar where it is used in requests.sessions
    with patch("requests.sessions.extract_cookies_to_jar") as mock_extract:
        # Define side effect to simulate cookie extraction
        def side_effect(jar, request, response):
            jar.set("session_id", "12345")
        
        mock_extract.side_effect = side_effect
        
        # Execute
        gen = session.resolve_redirects(resp, req)
        next(gen)
        
        # Verify extract_cookies_to_jar was called with the correct arguments
        mock_extract.assert_called_once()
        args, _ = mock_extract.call_args
        # args[0] is prepared_request._cookies
        # args[1] is prepared_request
        # args[2] is resp.raw
        assert args[1] == req
        assert args[2] == resp.raw
        
    # Verify the cookie was applied to the next request (via session.send)
    sent_request = session.send.call_args[0][0]
    assert "session_id" in sent_request._cookies
    assert sent_request._cookies["session_id"] == "12345"