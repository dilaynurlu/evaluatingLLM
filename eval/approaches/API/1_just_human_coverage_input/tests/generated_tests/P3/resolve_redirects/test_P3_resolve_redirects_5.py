import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.structures import CaseInsensitiveDict
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_does_not_leak_cookies_cross_domain():
    """
    Test that cookies scoped to the source domain are NOT sent to a different target domain.
    Critique addressed: Insufficient Cookie Scope Verification.
    """
    session = Session()
    # Setup a cookie strictly for 'example.com'
    jar = RequestsCookieJar()
    jar.set('session_cookie', 'secret_value', domain='example.com')
    session.cookies = jar
    
    # Target is a different domain
    target_resp = Response()
    target_resp.status_code = 200
    target_resp._content = b"OK"
    target_resp._content_consumed = True
    target_resp.url = "http://other.com/target"
    target_resp.raw = MagicMock()
    
    session.send = MagicMock(return_value=target_resp)
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/source")
    
    # Redirect to different domain
    resp = Response()
    resp.status_code = 302
    resp.headers = CaseInsensitiveDict({"Location": "http://other.com/target"})
    resp.url = "http://example.com/source"
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    resp.request = req
    
    # Execute
    list(session.resolve_redirects(resp, req))
    
    # Check the request headers sent to 'other.com'
    args, _ = session.send.call_args
    sent_req = args[0]
    
    # The session cookie for example.com should NOT be present
    cookie_header = sent_req.headers.get("Cookie", "")
    assert "session_cookie" not in cookie_header
    assert "secret_value" not in cookie_header