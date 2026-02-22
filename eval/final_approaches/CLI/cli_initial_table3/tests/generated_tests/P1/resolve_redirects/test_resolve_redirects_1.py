from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from unittest.mock import MagicMock, patch

def test_resolve_redirects_basic():
    session = Session()
    session.max_redirects = 5
    
    # Mock methods
    session.get_redirect_target = MagicMock(side_effect=["http://example.com/redirected", None])
    session.rebuild_method = MagicMock()
    session.rebuild_auth = MagicMock()
    session.rebuild_proxies = MagicMock()
    
    # Create response and request
    req = PreparedRequest()
    req.url = "http://example.com"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    
    resp = Response()
    resp.request = req
    resp.status_code = 302
    resp.url = "http://example.com"
    resp.raw = MagicMock()
    resp.close = MagicMock()
    
    # Mock send to return the next response
    next_resp = Response()
    next_resp.status_code = 200
    next_resp.url = "http://example.com/redirected"
    next_resp.history = []
    
    session.send = MagicMock(return_value=next_resp)
    
    gen = session.resolve_redirects(resp, req)
    
    # Should yield next_resp
    result_resp = next(gen)
    assert result_resp == next_resp
    
    # Verify send was called with new url
    args, kwargs = session.send.call_args
    sent_req = args[0]
    assert sent_req.url == "http://example.com/redirected"
    
    # Verify generator is exhausted
    try:
        next(gen)
        assert False, "Generator should be exhausted"
    except StopIteration:
        pass
