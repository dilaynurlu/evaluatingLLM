from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from unittest.mock import MagicMock

def test_resolve_redirects_relative_url():
    session = Session()
    session.max_redirects = 5
    
    # Mock redirect to relative path
    session.get_redirect_target = MagicMock(return_value="/foo")
    session.rebuild_method = MagicMock()
    session.rebuild_auth = MagicMock()
    session.rebuild_proxies = MagicMock()
    session.send = MagicMock()
    
    req = PreparedRequest()
    req.url = "http://example.com/base"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    
    resp = Response()
    resp.request = req
    resp.status_code = 302
    resp.url = "http://example.com/base"
    resp.raw = MagicMock()
    resp.close = MagicMock()
    
    next_resp = Response()
    next_resp.status_code = 200
    next_resp.url = "http://example.com/foo"
    next_resp.history = []
    
    session.send.return_value = next_resp
    
    gen = session.resolve_redirects(resp, req)
    
    result = next(gen)
    
    assert result == next_resp
    
    # Verify the URL was reconstructed correctly
    args, kwargs = session.send.call_args
    sent_req = args[0]
    assert sent_req.url == "http://example.com/foo"
