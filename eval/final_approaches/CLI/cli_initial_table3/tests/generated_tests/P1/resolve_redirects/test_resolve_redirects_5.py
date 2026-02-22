from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from unittest.mock import MagicMock

def test_resolve_redirects_yield_requests():
    session = Session()
    session.max_redirects = 5
    
    session.get_redirect_target = MagicMock(return_value="http://example.com/next")
    session.rebuild_method = MagicMock()
    session.rebuild_auth = MagicMock()
    session.rebuild_proxies = MagicMock()
    session.send = MagicMock()
    
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
    
    # Run generator with yield_requests=True
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    
    # Should yield a PreparedRequest
    result = next(gen)
    
    assert isinstance(result, PreparedRequest)
    assert result.url == "http://example.com/next"
    
    # Verify send was NOT called
    assert not session.send.called
