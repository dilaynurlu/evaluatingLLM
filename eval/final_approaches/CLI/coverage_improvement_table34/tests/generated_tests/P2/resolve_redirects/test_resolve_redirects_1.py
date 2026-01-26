from unittest.mock import Mock, ANY
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.structures import CaseInsensitiveDict
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_single():
    session = Session()
    
    # Initial response (301)
    resp = Response()
    resp.status_code = 301
    resp.headers = CaseInsensitiveDict({"Location": "http://example.com/new"})
    resp.url = "http://example.com/old"
    resp.raw = Mock()
    resp.raw.headers = resp.headers
    resp.raw.stream.return_value = [b""]
    
    # Original request
    req = PreparedRequest()
    req.method = "GET"
    req.url = "http://example.com/old"
    req.headers = CaseInsensitiveDict({})
    req._cookies = RequestsCookieJar()
    
    # Mock send to return a 200 OK
    resp_new = Response()
    resp_new.status_code = 200
    resp_new.url = "http://example.com/new"
    
    session.send = Mock(return_value=resp_new)
    
    gen = session.resolve_redirects(resp, req)
    history = list(gen)
    
    assert len(history) == 1
    assert history[0] == resp_new
    session.send.assert_called_with(ANY, stream=False, timeout=None, verify=True, cert=None, proxies={}, allow_redirects=False)
    assert session.send.call_args[0][0].url == "http://example.com/new"