from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from unittest.mock import MagicMock

def test_resolve_redirects_purge_headers():
    session = Session()
    session.max_redirects = 5
    
    session.get_redirect_target = MagicMock(return_value="http://example.com/next")
    session.rebuild_method = MagicMock()
    session.rebuild_auth = MagicMock()
    session.rebuild_proxies = MagicMock()
    
    # Original request with Content-Length
    req = PreparedRequest()
    req.url = "http://example.com"
    req.headers = {"Content-Length": "100", "Content-Type": "application/json", "User-Agent": "foo"}
    req._cookies = RequestsCookieJar()
    req.body = b"data"
    
    resp = Response()
    resp.request = req
    resp.status_code = 301 # Moved Permanently (should purge)
    resp.url = "http://example.com"
    resp.raw = MagicMock()
    resp.close = MagicMock()
    
    next_resp = Response()
    next_resp.status_code = 200
    
    session.send = MagicMock(return_value=next_resp)
    
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    # Check headers on the sent request
    args, kwargs = session.send.call_args
    sent_req = args[0]
    
    assert "Content-Length" not in sent_req.headers
    assert "Content-Type" not in sent_req.headers
    assert "User-Agent" in sent_req.headers
    assert sent_req.body is None

    # Now test with 307 (should NOT purge)
    req.headers = {"Content-Length": "100", "Content-Type": "application/json", "User-Agent": "foo"}
    req.body = b"data"
    resp.status_code = 307
    
    session.send.reset_mock()
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    args, kwargs = session.send.call_args
    sent_req = args[0]
    
    assert "Content-Length" in sent_req.headers
    assert "Content-Type" in sent_req.headers
    assert sent_req.body == b"data"
